import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

# Read in table from HTML content into pandas dataframe.
df = pd.read_html('https://www.worldometers.info/co2-emissions/co2-emissions-by-country/')[0]
# Drop extra id column and removing '%' symbols.
df = df.replace({'%': ''}, regex = True).drop(columns=['#'])
# Change values in '1 Year Change' and 'Share of world' columns to floats.
df = df.astype({'1 Year Change':'float', 'Share of world':'float'})

fig, axs = plt.subplots(1, 2, figsize = (20, 6))

axs[0].scatter(df['Population (2016)'].values, df['CO2 Emissions (tons, 2016)'].values)
axs[0].set_title('CO2 Emissions vs Population (2016)')
axs[0].set_xlabel('Population (2016)')
axs[0].set_ylabel('CO2 Emissions (tons, 2016)')

axs[1].scatter(df['Population (2016)'].values, df['CO2 Emissions (tons, 2016)'].values)
axs[1].set_title('CO2 Emissions vs Population (2016) (Logarithmic)')
axs[1].set_xlabel('Population (2016)')
axs[1].set_yscale('log')
axs[1].set_xscale('log')
axs[1].set_ylabel('CO2 Emissions (tons, 2016)')


def mcsim(df, N, alpha):
    '''
    Performs a Monte Carlo simulation to estimate the parameters β0 and β1 of a linear regression 
    model and their confidence intervals to fit a given dataset.
    
    Parameters:
        df (DataFrame) - A DataFrame object containing data to be used in the simulation.
        N (int) - The number of Monte Carlo simulations to compute.
        alpha (float) - The confidence level (e.g. 0.05 for a 95% confidence interval).
    
    Returns:
        params (DataFrame) - A DataFrame containing the estimated parameters β0 and β1 from each simulation.
    '''
    
    # Empty dataframe to store the estimated parameters.
    params = pd.DataFrame(columns = ['Intercept', 'Slope'])
    
    # Perform N Monte Carlo simulations.
    for i in range(N):
        
        # Resample the data.
        sample = df.sample(frac = 1, replace = True)
        
        # Perform linear regression model resampled data.
        X = sm.add_constant(sample['Population (2016)'].values)
        y = sample['CO2 Emissions (tons, 2016)'].values
        reg = sm.OLS(y, X).fit()
        
        # Store the estimates of parameters; β0 (intercept) and β1 (slope).
        params.loc[i] = reg.params
    
    return params


# ===============================================================
# Perform linear regression model on original data and standardise
# independent variable to make β coefficients more comparable.
# ===============================================================

# Normalise independent variable (x), mean = 0, std = 1
df['Population (2016)'] = (df['Population (2016)'] - df['Population (2016)'].mean()) / df['Population (2016)'].std()

X = sm.add_constant(df['Population (2016)'].values)
y = df['CO2 Emissions (tons, 2016)'].values
reg = sm.OLS(y, X).fit()


# ===============================================================
# Run Monte-Carlo simulation on resampled data for combinations of 
# N ∈ [100,500,100] and 𝛼 ∈ [0.01,0.05,0.1]. Then calculate the 
# confidence interval for each combination and the confidence 
# interval of the original data.
# ===============================================================

Ns = (100, 500, 1000)
alphas = (0.01, 0.05, 0.1)

params = {}
confint = {}
og_confint = {}

for i, N in enumerate(Ns):
    for j, alpha in enumerate(alphas):
        key = f'{N}_{alpha}'
        
        # Extract resampled confidence intervals for intercept and slope.
        params[key] = mcsim(df, N, alpha)
        confint[key] = params[key].quantile([alpha / 2, 1 - alpha / 2]).T
        
        # Extract original confidence intervals for intercept and slope.
        og_confint[key] = reg.conf_int(alpha)

        
# ===============================================================
# Plot histograms of parameters in a 3 x 3 array, with 
# increasing values of N and alpha.
# ===============================================================

for k, param in enumerate(['Intercept', 'Slope']):
    fig, axs = plt.subplots(3, 3, figsize = (20, 20))
    fig.suptitle(f'Monte Carlo Bootstrap Simulation (C02 Emissions (tons, 2016) / Population (2016)) - {param}', fontsize = 16)
    fig.subplots_adjust(top = 0.95)
    for i, N in enumerate(Ns):
        for j, alpha in enumerate(alphas):
            key = f'{N}_{alpha}'

            # Plot histogram of parameter.
            axs[i, j].hist(params[key][param], color = 'coral' if param == 'Intercept' else 'skyblue')
            axs[i, j].set_xlabel(fr'{param} - $\beta_0$' if param == 'Intercept' else fr'{param} - $\beta_1$')
            axs[i, j].set_ylabel('Frequency')
            axs[i, j].set_title(fr'N = {N}, $\alpha$ = {alpha}')

            # Add vertical lines for resampled confidence interval.
            axs[i, j].axvline(confint[key][alpha / 2][param], color='dimgray', linestyle='--', label = 'Approx. CI')
            axs[i, j].axvline(confint[key][1 - alpha / 2][param], color='dimgray', linestyle='--')

            # Add vertical lines for original confidence interval.
            axs[i, j].axvline(og_confint[key][k][0], color='black', linestyle='-', label='Exact CI')
            axs[i, j].axvline(og_confint[key][k][1], color='black', linestyle='-')

            axs[i, j].legend()
    fig.show()