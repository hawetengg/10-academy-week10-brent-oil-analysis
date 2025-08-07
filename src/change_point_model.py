import pandas as pd
import pymc as pm
import numpy as np
import matplotlib.pyplot as plt
import arviz as az

# Load data
df = pd.read_csv('data/BrentOilPrices.csv')
df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True)
df.set_index('Date', inplace=True)
df.dropna(inplace=True)
prices = df['Price'].values
n_points = len(prices)

# Bayesian Change Point Model
with pm.Model() as model:
    # Priors
    tau = pm.DiscreteUniform('tau', lower=0, upper=n_points-1)
    mu_1 = pm.Normal('mu_1', mu=np.mean(prices), sigma=20)
    mu_2 = pm.Normal('mu_2', mu=np.mean(prices), sigma=20)
    sigma = pm.HalfNormal('sigma', sigma=10)

    # Switch function
    idx = np.arange(n_points)
    mu = pm.math.switch(tau > idx, mu_1, mu_2)

    # Likelihood
    observation = pm.Normal('obs', mu=mu, sigma=sigma, observed=prices)

    # Sampling
    trace = pm.sample(2000, tune=1000, return_inferencedata=False)

# Check convergence
summary = az.summary(trace)
print(summary)
az.plot_trace(trace)
plt.savefig('../docs/trace_plot.png')
plt.close()

# Plot posterior of tau
tau_posterior = trace['tau']
plt.hist(tau_posterior, bins=50, density=True)
plt.title('Posterior Distribution of Change Point (tau)')
plt.xlabel('Index')
plt.ylabel('Density')
plt.savefig('../docs/tau_posterior.png')
plt.close()

# Convert tau to date
tau_mean = int(np.mean(tau_posterior))
change_date = df.index[tau_mean]
print(f'Most likely change point: {change_date}')

# Quantify impact
mu_1_mean = np.mean(trace['mu_1'])
mu_2_mean = np.mean(trace['mu_2'])
print(f'Mean price before: ${mu_1_mean:.2f}, after: ${mu_2_mean:.2f}')
print(f'Price change: {((mu_2_mean - mu_1_mean) / mu_1_mean) * 100:.2f}%')

# Plot prices with change point
plt.figure(figsize=(12, 6))
plt.plot(df.index, prices, label='Brent Oil Price')
plt.axvline(change_date, color='red', linestyle='--', label=f'Change Point: {change_date.date()}')
plt.title('Brent Oil Prices with Detected Change Point')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.savefig('../docs/change_point_plot.png')
plt.close()