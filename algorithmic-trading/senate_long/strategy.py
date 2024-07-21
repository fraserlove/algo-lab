import argparse
import keyring
import datetime
import time
import pandas as pd

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from scraper import SenateScraper

class Strategy:

    def __init__(self, live: bool, position_length: int, rebalance_frequency: int):
        self.live = live # Use paper trading, no real money used.
        self.position_length = position_length # Number of days to hold a trade.
        self.rebalance_frequency = rebalance_frequency # Number of days to wait between rebalancing.

        print(f'INFO: Running strategy. LIVE: {live}. POSITION_LENGTH: {position_length}. REBALANCE_FREQUENCY: {rebalance_frequency}')


    def timestamp(self) -> datetime.datetime:
        ''' Returns the current market time adjusted to UTC. '''
        return self.trade_client.get_clock().timestamp
    

    def run(self):
        ''' Runs the strategy, performing an initial rebalance and then rebalancing accordingly. '''

        self.trade_client = self._load_client()
        # Perform initial balancing of portfolio now.
        self.next_rebalance = self.timestamp()

        self.fund_details()
        while True:
            self.rebalance()
            self.fund_details()
            self.wait_for_rebalance()


    def _load_client(self) -> TradingClient:
        '''
        Load the Alpaca trading client.

        :return: An instance of the Alpaca TradingClient.
        '''

        if self.live:
            print('WARNING: Live Trading.')

        # Fetch Alpaca API keys from Apple keychain.
        (api_key_type, secret_key_type) = ('api_key', 'secret_key') if self.live else ('api_key_paper', 'secret_key_paper')
        api_key = keyring.get_password('alpaca', api_key_type)
        secret_key = keyring.get_password('alpaca', secret_key_type)

        if not api_key or not secret_key:
            raise Exception('Alpaca API key not found.')

        paper = not self.live
        return TradingClient(api_key, secret_key, paper=paper)


    def load_orders(self) -> pd.DataFrame:
        '''
        Load and process trading orders.
        
        :return: A DataFrame containing trading orders.
        '''

        orders = SenateScraper().senate_trading(lookback_period=self.position_length, tx_type='Purchase')
        # Weighting stocks to buy based on the aggregate of the dollar amount purchased.
        equity = float(self.trade_client.get_account().equity)
        orders.loc[:, 'weighted_amount'] = orders['tx_amount'] / orders['tx_amount'].sum() * equity
        return orders


    def buy_orders(self, orders: pd.DataFrame) -> None:
        '''
        Initialise buy orders based on the provided DataFrame of orders.
        
        :param orders_df: A DataFrame containing trading orders.
        '''

        print(f'INFO: {self.timestamp()}: Initiating {len(orders)} buy orders...')
        for _, order in orders.iterrows():
            ticker = order['ticker']

            # Check asset is fractionable through Alpaca.
            if self.trade_client.get_asset(ticker).fractionable:
                # Round amount to comply with Alpaca fractional trading limits.
                amount = round(order['weighted_amount'], 2)
                order = self.trade_client.submit_order(
                    order_data = MarketOrderRequest(
                        symbol=ticker,
                        notional=amount,
                        side=OrderSide.BUY,
                        time_in_force=TimeInForce.DAY
                    )
                )
                print(f'BUY: ${order.notional} of {order.symbol}')
            else:
                print(f'INFO: Skipping {ticker}. Not fractionable via Alpaca.')
        print(f'INFO: {self.timestamp()}: All {len(orders)} orders initiated.')


    def close_all(self) -> None:
        ''' Sell all positions and close all orders. '''

        print('INFO: Closing all positions.')
        self.trade_client.close_all_positions(cancel_orders=True)


    def fund_details(self) -> None:
        ''' Print details about the funds state. '''

        account = self.trade_client.get_account()
        positions = self.trade_client.get_all_positions()

        print(f'\n========== Fund Details ==========')
        print(f'Current Time: {self.timestamp()}')
        print(f'Fund Equity: ${float(account.equity):.2f}')
        print(f'Last Equity: ${float(account.last_equity):.2f}')
        print(f'Cash: ${float(account.cash):.2f}')
        print(f'Fees: ${float(account.accrued_fees):.2f}')
        print(f'Open Positions: {len(positions)}')
        print(f'Currency: {account.currency}')
        print(f'Next Rebalance: {self.next_rebalance}')
        print(f'==================================\n')


    def wait_for_rebalance(self) -> None:
        ''' Wait until the next rebalance is due. '''

        print(f'INFO: {self.timestamp()}: Waiting for next rebalance ({self.next_rebalance})...')
        try:
            time.sleep((self.next_rebalance - self.timestamp()).total_seconds())
        except KeyboardInterrupt:
            print('Exiting strategy...'); raise SystemExit
        print(f'INFO: {self.timestamp()}: Reblance due. Awakening...')


    def rebalance(self):
        ''' Perform the rebalancing process by selling all assets and creating new orders. '''

        print(f'INFO: {self.timestamp()}: Initiating Rebalance...')
        try:
            self.close_all()
            orders = self.load_orders()
            self.buy_orders(orders)
            # Update the time until the next rebalance is due.
            self.next_rebalance += datetime.timedelta(days=self.rebalance_frequency)
        except:
            print('ERROR: Rebalance failed. Trying again at next market open.')
            self.next_rebalance = self.clock.next_open
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run the senate long strategy with optional arguments.')
    parser.add_argument('--live', default=False, action=argparse.BooleanOptionalAction, help='Trade with live funds or a paper account.')
    parser.add_argument('--position_length', default=60, type=int, help='Number of days to hold a trade.')
    parser.add_argument('--rebalance_frequency', default=7, type=int, help='Number of days to wait between rebalancing.')

    args = parser.parse_args()
    
    senate_long = Strategy(args.live, args.position_length, args.rebalance_frequency)
    senate_long.run()