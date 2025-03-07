import bs4
import pandas as pd
import datetime
import requests

class SenateScraper():

    # URLs for the Senate Electronic Financial Disclosure (EFD) search.
    ROOT = 'https://efdsearch.senate.gov'
    LANDING_URL = f'{ROOT}/search/home/'
    SEARCH_URL = f'{ROOT}/search/'
    REPORTS_URL = f'{ROOT}/search/report/data/'

    BATCH_SIZE = 100 # Number of records to process in a single batch. Must be max of 100.

    # Header names for the columns in the generated dataframe.
    HEADER = ['senator', 'tx_date', 'file_date', 'ticker', 'type', 'tx_amount']

    def __init__(self):
        self.client = requests.Session() # A `requests.Session` object representing the client's session.


    def _set_csrf(self) -> str:
        '''
        Set the session ID and return the CSRF token for this session.
        
        :return: The CSRF token to include in the request for authentication.
        '''

        try:
            # Fetch the landing page using the client session.
            landing_page = bs4.BeautifulSoup(self.client.get(SenateScraper.LANDING_URL).text, 'lxml')
            # Extract the CSRF token from the HTML form on the landing page.
            form_csrf = landing_page.find(attrs={'name': 'csrfmiddlewaretoken'})['value']
            # Prepare the payload for the form submission including the CSRF token.
            form_payload = { 'csrfmiddlewaretoken': form_csrf, 'prohibition_agreement': '1' }
            # Submit the form using a POST request to set the session's CSRF token.
            self.client.post(SenateScraper.LANDING_URL, data=form_payload, headers={'Referer': SenateScraper.LANDING_URL})
            # Set the CSRF token from the session cookies.
            return self.client.cookies['csrftoken'] if 'csrftoken' in self.client.cookies else self.client.cookies['csrf']
        except:
            print('ERROR: Unable to load CSRF token for EFD search.')


    def _fetch_reports(self, offset: int, lookback_period: int) -> list[list[str]]:
        '''
        Query the periodic transaction reports API and return the fetched data.

        :param offset: The starting index of the reports to fetch.
        :param lookback_period: Lookback period (in days) to search for records.
        :return: A list of lists containing the fetched transaction report data.
        '''
        
        # Only request reports that were made within the lookback period.
        cutoff = (datetime.datetime.now() - datetime.timedelta(days=lookback_period)).strftime('%m/%d/%Y')
        login_data = {
            'start': str(offset),
            'length': str(SenateScraper.BATCH_SIZE),
            'report_types': '[11]',
            'submitted_start_date': f'{cutoff} 00:00:00',
            'csrfmiddlewaretoken': self._set_csrf()
        }
        # Send a POST request to the reports API to fetch the data.
        response = self.client.post(SenateScraper.REPORTS_URL, data=login_data, headers={'Referer': SenateScraper.SEARCH_URL})
        if not response.status_code == 200:
            print(f'ERROR: Failed to fetch senate trading data: {response.status_code} error.')
            return []
        # Extract and return the data from the response in JSON format.
        return response.json()['data']


    def _fetch_tbody(self, link: str) -> bs4.element.Tag:
        '''
        Returns the tbody element containing transactions for this senator.

        :param link: The relative link to the senator's report.
        :return: A `bs4.element.Tag` representing the tbody element.
        '''

        # Construct the full URL for the senator's report using the provided link.
        report_url = f'{SenateScraper.ROOT}{link}'
        report_response = self.client.get(report_url)
        report = bs4.BeautifulSoup(report_response.text, 'lxml')
        # Return the first tbody instance, which contains the transaction data.
        return report.find('tbody')


    def _fetch_txs(self, row: list[str], lookback_period: int, tx_type: str) -> pd.DataFrame:
        '''
        Convert a row from the periodic transaction reports API to a DataFrame
        of transactions.

        :param row: A list representing a row of data from the periodic transaction reports API.
        :param lookback_period: Lookback period (in days) to search for records.
        :param tx_type: The type of transaction to filter for.
        :return: A DataFrame containing transaction data.
        '''

        # Extract relevant data from the row.
        first, last, _, link_html, file_date = row
        # Parse the link HTML to extract the report link.
        link = bs4.BeautifulSoup(link_html, 'lxml').a.get('href')
        # Fetch the tbody element containing transactions from the report.
        tbody = self._fetch_tbody(link)

        stocks = []
        # Calculate cutoff date so only transactions within the lookback period are included.
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=lookback_period)
        # Check that tbody exists.
        if tbody:
            # Iterate through each table row within the tbody.
            for table_row in tbody.find_all('tr'):
                # Extract data from each column of the table row.
                cols = [c.get_text() for c in table_row.find_all('td')]

                # Extract relevant transaction details from the columns.
                tx_amount = int(cols[7].split('$')[-1].replace(',', ''))
                tx_date = cols[1].strip()
                ticker = cols[3].strip()
                order_type = cols[6].strip()

                # Append transaction details to the 'stocks' list. Removing instances of null tickers.
                if ticker.strip() not in ('--', ''):
                    # Filter out trades that were not stock purchases made within the position length.
                    if datetime.datetime.strptime(tx_date, '%m/%d/%Y') >= cutoff_date:
                        # Filter out trades that are not of the correct transaction type.
                        if order_type == tx_type:
                            stocks.append([f'{first} {last}', tx_date, file_date, ticker, order_type, tx_amount])             
                    
        # Create a DataFrame from the 'stocks' list and rename columns using HEADER.
        return pd.DataFrame(stocks).rename(columns=dict(enumerate(SenateScraper.HEADER)))


    def _senator_reports(self, lookback_period: int) -> list[list[str]]:
        '''
        Fetch and return all results from the periodic transaction reports API.

        :param lookback_period: Lookback period (in days) to search for records.
        :param tx_type: The type of transaction to filter for.
        :return: A list of lists containing the transaction report data.
        '''

        i = 0
        all_reports = []
        # Fetch the initial batch of reports from the API.
        reports = self._fetch_reports(i, lookback_period)
        
        # Fetch reports from the API in batches until no more reports are received.
        while len(reports):
            # Extend the list of all_reports with the reports fetched in this batch.
            all_reports.extend(reports)
            # Move to the next batch.
            i += SenateScraper.BATCH_SIZE
            # Fetch reports for the current batch.
            reports = self._fetch_reports(i, lookback_period)
        return all_reports


    def senate_trading(self, lookback_period: int, tx_type: str) -> pd.DataFrame:
        '''
        Search for senate trades, fetch transaction data, and return as a DataFrame.

        :param lookback_period: Lookback period (in days) to search for records.
        :return: A DataFrame containing senate trading transaction data.
        '''

        print(f'INFO: Searching for senate trades. LOOKBACK_PERIOD: {lookback_period}. TX_TYPE: {tx_type}.')
        # Fetch reports containing Senate trading data.
        reports = self._senator_reports(lookback_period)

        all_txs = pd.DataFrame()
        # Loop through each report and fetch transaction data.
        for report in reports:
            # Fetch transactions for the current report.
            txs = self._fetch_txs(report, lookback_period, tx_type)
            # Check that transactions are present.
            if not txs.empty:
                # Concatenate the fetched transactions to the overall DataFrame.
                all_txs = pd.concat([all_txs, pd.DataFrame(txs)], ignore_index=True)

                file_date = datetime.datetime.strptime(report[4], '%m/%d/%Y').strftime('%Y-%m-%d')
                print(f'INFO: Fetched Report ({file_date}). {report[0]} {report[1]}. {len(txs)} trades.')

        # Convert 'tx_date' and 'file_date' columns to datetime objects.
        all_txs['tx_date'] = pd.to_datetime(all_txs['tx_date'])
        all_txs['file_date'] = pd.to_datetime(all_txs['file_date'])

        print(f'INFO: Found {len(all_txs)} trades.')
        # Sort transactions by 'tx_date' in descending order and return the DataFrame.
        return all_txs.sort_values('tx_date', ascending=False)