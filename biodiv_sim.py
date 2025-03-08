import numpy as np
from scipy import stats
import pandas as pd

np.random.seed(42)
n_iter = 1000000

# Climate (Simplified - Climate change assumed to occur)
climate_loss_mean = np.log(0.215)
climate_loss_std = (np.log(0.29) - np.log(0.14)) / 4
climate_loss = stats.lognorm(s=climate_loss_std, scale=np.exp(climate_loss_mean)).rvs(n_iter)
climate_impact = np.minimum(climate_loss, 1.0)

# Nuclear
nuclear_annual_risk = 0.01  # Updated to 1% annual risk based on search results
nuclear_years = 50
nuclear_prob = 1 - np.exp(-nuclear_annual_risk * nuclear_years)
nuclear_occurs = np.random.binomial(1, nuclear_prob, n_iter)
nuclear_loss = 0.50
nuclear_impact = nuclear_occurs * nuclear_loss

# Cosmic
cosmic_lambda = 100 / 50000
cosmic_occurs = np.random.poisson(cosmic_lambda, n_iter)
cosmic_loss = 0.70
cosmic_impact = (cosmic_occurs > 0) * cosmic_loss

# Cascade (More meaningful amplification)
cascade_factor = 1 + 0.5 * climate_impact  # Adjust scaling factor (0.5) as needed
uncapped_loss = climate_impact + (nuclear_impact + cosmic_impact) * cascade_factor
total_loss = np.minimum(uncapped_loss, 1.0)

# Debug
print(f"Uncapped Mean: {np.mean(uncapped_loss) * 100:.1f}%")
print(f"Max Uncapped: {np.max(uncapped_loss) * 100:.1f}%")
print(f"% Runs Capped: {np.mean(uncapped_loss >= 1.0) * 100:.1f}%")
print(f"Mean Loss: {np.mean(total_loss) * 100:.1f}%")
print(f"95% CI: {np.percentile(total_loss, [2.5, 97.5])[0] * 100:.1f}% – {np.percentile(total_loss, [2.5, 97.5])[1] * 100:.1f}%")
print(f"Climate: {np.mean(climate_impact) * 100:.1f}%")
print(f"Nuclear: {np.mean(nuclear_impact) * 100:.1f}%")
print(f"Cosmic: {np.mean(cosmic_impact) * 100:.1f}%")

results = pd.DataFrame({
    "Total Loss": total_loss,
    "Climate Impact": climate_impact,
    "Nuclear Impact": nuclear_impact,
    "Cosmic Impact": cosmic_impact
})
results.to_csv("biodiv_results_corrected_v2.csv", index=False) # Saved to a new file