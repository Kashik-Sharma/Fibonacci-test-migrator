# J. Pocahontas Olson   June 2016
# An API simulating a source of Fibonacci numbers with some noise.
#   For instance, poorly defined bumps on tree trunks, a hard to measure bunny population,
#   visual scan of arrangement of sunflower seeds, or any other system where you
#   know your values are fibonacci numbers, but some noise has been introduced in your measurement.

import fibonacci_module as fb         # Custom module made for this project
import numpy as np
import random
from logger_config import logger

# Constants to set range of Fibonacci numbers, and gaussian noise
FIB_MAX = 1000
GAUSSIAN_MEAN = 1
GAUSSIAN_STDEV = 0.1



## Add Gausian noise to simulate real-world data collection.
#   Noise scales by size of number to mimic that you're likely to be more
#   precise if you have a few to count, and off by more when there are large
#   numbers involved.
def add_noise(list_of_pure_data):
    logger.info("Adding Gaussian noise to data.")
    noisy_data = []
    for i in range(len(list_of_pure_data)):
        noisy_data.append(np.random.normal(GAUSSIAN_MEAN,GAUSSIAN_STDEV,1)[0]*list_of_pure_data[i])
    
    return noisy_data


## API call, mimicking real-world data collection
def get_data(how_much):
    logger.info(f"Generating {how_much} random Fibonacci numbers with noise.")
    # Get how_much random Fibonacci numbers
    fibnumbers = fb.fibList(FIB_MAX)
    data = []
    for _ in range(how_much):
        data.append(fibnumbers[random.randrange(1, FIB_MAX, 1)])
    
    # Add Gausian noise to simulate real-world data
    add_noise(data)

    return data




if __name__ == "__main__":
    SHOW_THIS_MANY = 20
    logger.info(f"..Obtaining {SHOW_THIS_MANY} data points, with values obtained from the first {FIB_MAX}")
    logger.info(f"..Fibonacci numbers, with Gaussian noise of mean {GAUSSIAN_MEAN} and standard deviation {GAUSSIAN_STDEV}.")
    print(get_data(SHOW_THIS_MANY))