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
    """This function generates an exponential random variable with the provided parameters using inverse transform.

    Parameters----
    lmbda : the 1/scale parameter for your exponential distribution
    """

    random_number = np.random.uniform(low = 0.0, high = 1.0)
    return - (1 / lmbda) * np.log(random_number)


def generate_exponential_antithetic(lmbda: float):
    """This function generates an exponential random variable with the provided parameters using inverse transform.
    Uses antithetic variables.

    Parameters----
    lmbda : the 1/scale parameter for your exponential distribution
    """

    random_number = np.random.uniform(low = 0.0, high = 1.0)
    return ((- (1 / lmbda) * np.log(1 - random_number)) + (- (1 / lmbda) * np.log(random_number))) / 2


def generate_normal(loc: float = 0, scale: float = 1):
    """This function generates an normal random variable with the provided parameters.

    Parameters----
    loc : the mean of your normal distribution
    scale : the standard deviation of your normal distribution
    """

    random_number = np.random.uniform(low = 0.0, high = 1.0)
    return stats.norm.ppf(q = random_number, scale = scale, loc = loc)


def generate_binomial(n: int, p: float = 0.5):
    """This function generates a binomial random variable with the provided parameters.

    Parameters----
    n : the number of trials
    p: the probability of a trial being successfull
    """

    random_number = np.random.uniform(low = 0.0, high = 1.0)
    return stats.binom.ppf(q = random_number, n = n, p = p)
    
def generate_binomial_antithetic(n: int, p: float = 0.5):
    """This function generates a binomial random variable with the provided parameters.
    Uses antithetic variables.

    Parameters----
    n : the number of trials
    p: the probability of a trial being successfull
    """

    random_number = np.random.uniform(low = 0.0, high = 1.0)
    return (stats.binom.ppf(q = random_number, n = n, p = p) + stats.binom.ppf(q = 1 - random_number, n = n, p = p)) / 2
