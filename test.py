from inverse_transform_sampling import *
import numpy as np
import scipy.stats as stats

# variance reduction techniques:
# original: MC
# 1: antithetic variables
# 2: variance reduction by conditioning
# control variates
# stratified sampling
# importance sampling

print("Hello!")

samples = 1000
iterations = 100
a_list = []
b_list = []

def exp(lmbda):
    randomNumber = np.random.uniform(low = 0.0, high = 1.0)
    return - (1 / lmbda) * np.log(randomNumber)

def exp_antithetic(lmbda):
    randomNumber = np.random.uniform(low = 0.0, high = 1.0)
    return ((- (1 / lmbda) * np.log(1 - randomNumber)) + (- (1 / lmbda) * np.log(randomNumber))) / 2

for i in range(iterations):
    a = [exp(5) for _ in range(samples)]
    # a = [generate_exponential(5) for _ in range(samples)]
    # a_list.append(np.mean(a))
    a_list.extend(a)
    if i % 2 == 0:
        b = [exp_antithetic(5) for _ in range(samples)]
        # b = [generate_exponential_antithetic(5) for _ in range(samples)]
        # b_list.append(np.mean(b[0]))
        # b_list.append(np.mean(b[1]))
        # b0, b1 = zip(*b)
        b_list.extend(b)
        # b_list.extend(b1)

print(f"Stats for a are len={len(a_list)}, mean={np.mean(a_list)} and std={np.std(a_list)} with variance={np.std(a_list) ** 2}")
print(f"Stats for b are len={len(b_list)}, mean={np.mean(b_list)} and std={np.std(b_list)} with variance={np.std(b_list) ** 2}")