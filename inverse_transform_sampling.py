import numpy as np
import pandas as pd
import scipy.stats as stats

def generateExponential(lmbda: float):
    """This function generates an exponential random variable with the provided parameters.

    Parameters----
    lmbda : the 1/scale parameter for your exponential distribution
    """

    randomNumber = np.random.uniform(low = 0.0, high = 1.0)
    return stats.expon.ppf(q = randomNumber, scale = 1 / lmbda)


def generateNormal(loc: float = 0, scale: float = 1):
    """This function generates an normal random variable with the provided parameters.

    Parameters----
    loc : the mean of your normal distribution
    scale : the standard deviation of your normal distribution
    """

    randomNumber = np.random.uniform(low = 0.0, high = 1.0)
    return stats.norm.ppf(q = randomNumber, scale = scale, loc = loc)


def generateBinomial(n: int, p: float = 0.5):
    """This function generates a binomial random variable with the provided parameters.

    Parameters----
    n : the number of trials
    p: the probability of a trial being successfull
    """

    randomNumber = np.random.uniform(low = 0.0, high = 1.0)
    return stats.binom.ppf(q = randomNumber, n = n, p = p)
