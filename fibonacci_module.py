# J. Pocahontas Olson  June 2016
# Module containing function definitions relating to the Fibonacci numbers

import math
import os.path
import distutils.util
import logging

# Configure logger for this module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# A check to ensure that inputs are positive integers, which most of these functions require
def ensure_positive_int(num):
    # Make sure it's an integer
    try:
        val = int(num)
    except ValueError:
        logger.error("Could not interpret input as an integer", exc_info=True)
        raise ValueError("Could not interpret your input as an integer")
    
    # Make sure it's positive
    if val < 0:
        logger.error("Input is not positive: %d", val)
        raise ValueError(num, ' is not positive.')
    
    return val

# For a given integer n, print out the first n Fibonacci numbers
def fibList(num):
    try:
        num = ensure_positive_int(num)
    except ValueError:
        logger.warning("Invalid input for Fibonacci list generation: %s", num)
        return []
    
    fibNumbers = []
    
    if num >= 1:
        fibNumbers.append(0)
    if num >= 2:
        fibNumbers.append(1)
    if num > 2:  # assert: fibNumbers = [0, 1]
        i=2
        while i <= num-1:  # -1 adjusts for zero-indexing
            fibNumbers.append( fibNumbers[i-2] + fibNumbers[i-1] )
            i += 1
    if num < 0:
        logger.error("Invalid input. %d should be a positive integer.", num)
        raise ValueError('Invalid input. ', num, ' should be a positive integer.')
    
    return fibNumbers

####  Theoretical Predictions  ####
# Binet's formula gives a closed form expression for the nth Fibonacci number,
#   see https://en.wikipedia.org/wiki/Fibonacci_number#Closed-form_expression
# We can also invert Binet's formula to get n for a given Fibonacci number,
#   see https://en.wikipedia.org/wiki/Fibonacci_number#Recognizing_Fibonacci_numbers
# These functions are defined below

# Golden ratio definitions
phi = (1+math.sqrt(5))/2
psi = (1-math.sqrt(5))/2

# A function to determine if a number is a perfect square
def is_square(integer):
    integer = ensure_positive_int(integer)
    
    root = math.sqrt(integer)
    if int(root + 0.5) ** 2 == integer:  # int() floors it, and adding .5 is so 2.999 & 3.001 (i.e.) map to 3
        return True
    else:
        return False

# A function to determine if a number is a fibonacci number
#   For more info, refer to https://en.wikipedia.org/wiki/Fibonacci_number#Recognizing_Fibonacci_numbers
def is_fibonacci(integer):
    integer = ensure_positive_int(integer)
    return (is_square(5*math.pow(integer, 2) + 4) or is_square(5*math.pow(integer, 2) - 4))

# Binet's formula, to find the position in the sequence of a given Fibonacci number
#  If input is a fibonacci number, this will return an int.
#  Otherwise, it'll return a float which can be rounded to find the nearest fibonacci number.
def n_Binet(input):
    input = ensure_positive_int(input)
    if (input == 0):
        return (1, 1)  # 0 is the first Fibonacci number
    numerator_plus  = input*math.sqrt(5) + math.sqrt(5*math.pow(input,2) + 4)
    numerator_minus = input*math.sqrt(5) + math.sqrt(5*math.pow(input,2) - 4)
    n_plus  = math.log(numerator_plus /2, phi)
    n_minus = math.log(numerator_minus/2, phi)

    # Fibonacci numbers have perfect square, so use that if that's the case
    if is_square(numerator_plus):
        return (n_plus, n_plus)
    elif is_square(numerator_minus):
        return (n_minus, n_minus)
    else:
        return (n_plus, n_minus)

# Binet's formula to find the nth Fibonacci number
def f_Binet(nth):
    nth = ensure_positive_int(nth)
    if (nth == 0):
        logger.error("Zero not valid. Indexing is such that 1st Fib num is 0, 2nd is 1, etc.")
        raise ValueError("Zero not valid. Indexing is such that 1st Fib num is 0, 2nd is 1, etc.")
    if (nth == 1):
        return 0  # 0 is the first Fibonacci number
    # Account for indexing (1st Fib num is 0, 2nd is 1, etc.)
    nth -= 1
    
    return round((math.pow(phi, nth) - math.pow(psi, nth))/math.sqrt(5))

# Nudges a non-fibonacci number to the closest fibonacci number
def nearest_Binet_fib(input):
    input = ensure_positive_int(input)
    if (input == 0):
        return 0  # 0 is the first Fibonacci number
    
    (n_plus, n_minus) = n_Binet(input)
    if ( round(n_plus) == round(n_minus) ):
        return f_Binet(round(n_plus))
    else:
        fib_plus  = f_Binet(round(n_plus ))
        fib_minus = f_Binet(round(n_minus))
        if ( abs(fib_plus - input) < abs(fib_minus - input) ):
            return fib_plus
        else:
            return fib_minus

####  Saving Values  ####
# Trying to be more efficient by saving off values of fibonacci numbers ahead of time
NUMBER_OF_BYTES = 16384   # 4 bytes = 32 bit, 8 bytes = 64 bit, ... (fib gets big fast)
MAX_NUMBER_OF_SAVED_DIGITS = int(1e5)  # If want to store more, will have to increase NUMBER_OF_BYTES
filename = 'savedFibonacciNumbers.bin'

# Stores off the first MAX_NUMBER_OF_DIGITS Fibonacci numbers to a file, to store processing time
def make_saved_Fibonacci_file():
    logger.info("Making a binary file with the first %d Fibonacci numbers.", MAX_NUMBER_OF_SAVED_DIGITS)
    # See if file exists already, and warn
    if os.path.isfile(filename):
        prompt = "Warning: " + filename + " already exists with " + str(os.path.getsize(filename)/NUMBER_OF_BYTES)
        prompt += " digits.
  Do you wish to overwrite?: (Y/N) "
        ans = input(prompt)
        overwrite = distutils.util.strtobool(ans)
        if not overwrite:
            logger.info("..Exiting without writing over %s..", filename)
            return

    savedList = fibList(MAX_NUMBER_OF_SAVED_DIGITS)
    
    # Write binary data to a file
    with open(filename, 'wb') as f:
        for num in savedList:
            f.write(num.to_bytes(NUMBER_OF_BYTES, byteorder='big', signed=False))

# Remaining methods will have logging added similarly