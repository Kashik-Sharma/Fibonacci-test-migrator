# J. Pocahontas Olson   June 2016
# An API simulating a source of Fibonacci numbers with some noise.
#   For instance, poorly defined bumps on tree trunks, a hard to measure bunny population,
#   visual scan of arrangement of sunflower seeds, or any other system where you
#   know your values are fibonacci numbers, but some noise has been introduced in your measurement.

import fibonacci_module as fb         # Custom module made for this project
import numpy as np
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants to set range of Fibonacci numbers, and gaussian noise
FIB_MAX = 1000
GAUSSIAN_MEAN = 1
GAUSSIAN_STDEV = 0.1

## Add Gaussian noise to simulate real-world data collection.
#   Noise scales by size of number to mimic that you're likely to be more
#   precise if you have a few to count, and off by more when there are large
#   numbers involved.
def add_noise(list_of_pure_data):
    logger.info("Adding Gaussian noise to the dataset.")
    noisy_data = []
    for i in range(len(list_of_pure_data)):
        noisy_data.append(np.random.normal(GAUSSIAN_MEAN, GAUSSIAN_STDEV, 1)[0] * list_of_pure_data[i])
    return noisy_data

## API call, mimicking real-world data collection
def get_data(how_much):
    logger.info("Fetching Fibonacci data with noise.")
    # Get how_much random Fibonacci numbers
    fibnumbers = fb.fibList(FIB_MAX)
    data = []
    for i in range(how_much):
        data.append(fibnumbers[random.randrange(1, FIB_MAX, 1)])

    # Add Gaussian noise to simulate real-world data
    noisy_data = add_noise(data)

    return noisy_data

if __name__ == "__main__":
    SHOW_THIS_MANY = 20
    logger.info("Obtaining %d data points, with values from the first %d Fibonacci numbers and Gaussian noise.", SHOW_THIS_MANY, FIB_MAX)
    logger.info("Data: %s", get_data(SHOW_THIS_MANY))