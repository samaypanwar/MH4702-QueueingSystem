import numpy as np
import scipy.stats as stats

# variance reduction techniques:
# original: MC
# 1: antithetic variables
# 2: variance reduction by conditioning
# control variates
# stratified sampling
# importance sampling

def generate_exponential(lmbda: float):
    """This function generates an exponential random variable with the provided parameters.

    Parameters----
    lmbda : the 1/scale parameter for your exponential distribution
    """

    randomNumber = np.random.uniform(low = 0.0, high = 1.0)
    return stats.expon.ppf(q = randomNumber, scale = 1 / lmbda)

for interarrival_times, serving_times in zip(zip(*[[0,1],[2,3],[4,5]]), zip(*[[7,8],[9,10],[11,12]])):
    print(list(interarrival_times), list(serving_times))