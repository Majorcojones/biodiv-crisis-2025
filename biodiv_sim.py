import numpy as np
from scipy import stats
import pandas as pd

np.random.seed(42)
n_iter = 10000

# Climate: 70–80% prob, 14–29% loss (log-normal)
climate_prob = stats.uniform(0.7, 0.1).rvs(n_iter)
climate_loss_mean = np.log(21.5)
climate_loss_std = (np.log(29) - np.log(14)) / 4
climate_loss = stats.lognorm(s=climate_loss_std, scale=np.exp(climate_loss_mean)).rvs(n_iter)
climate_occurs = np.random.binomial(1, climate_prob)
climate_impact = climate_occurs * climate_loss

# Nuclear: ~25% over 50 years, 50% loss
nuclear_annual_risk = 0.0065
nuclear_years = 50
nuclear_prob = 1 - np.exp(-nuclear_annual_risk * nuclear_years)
nuclear_occurs = np.random.binomial(1, nuclear_prob, n_iter)
nuclear_loss = 0.50
nuclear_impact = nuclear_occurs * nuclear_loss

# Cosmic: 0.1% per century, 70% loss
cosmic_lambda = 100 / 50000
cosmic_occurs = np.random.poisson(cosmic_lambda, n_iter)
cosmic_loss = 0.70
cosmic_impact = (cosmic_occurs > 0) * cosmic_loss

# Cascade: Climate boosts others by 20%
cascade_factor = 1 + 0.2 * climate_occurs
total_loss = np.minimum(climate_impact + (nuclear_impact + cosmic_impact) * cascade_factor, 1.0)

# Results
mean_loss = np.mean(total_loss) * 100
ci_95 = np.percentile(total_loss, [2.5, 97.5]) * 100
climate_contrib = np.mean(climate_impact) * 100
nuclear_contrib = np.mean(nuclear_impact) * 100
cosmic_contrib = np.mean(cosmic_impact) * 100

print(f"Mean Loss: {mean_loss:.1f}%")
print(f"95% CI: {ci_95[0]:.1f}% – {ci_95[1]:.1f}%")
print(f"Climate: {climate_contrib:.1f}%")
print(f"Nuclear: {nuclear_contrib:.1f}%")
print(f"Cosmic: {cosmic_contrib:.1f}%")

# Save
results = pd.DataFrame({
    "Total Loss": total_loss,
    "Climate Impact": climate_impact,
    "Nuclear Impact": nuclear_impact,
    "Cosmic Impact": cosmic_impact
})
results.to_csv("biodiv_results.csv", index=False)