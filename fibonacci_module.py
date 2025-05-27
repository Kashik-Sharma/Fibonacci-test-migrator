# J. Pocahontas Olson  June 2016
# Module containing function definitions relating to the Fibonacci numbers

import math
from logger_config import logger

# A check to ensure that inputs are positive integers, which most of these functions require
def ensure_positive_int(num):
    # Make sure it's an integer
    try:
        val = int(num)
    except ValueError:
        logger.error("Could not interpret input as an integer.")
        raise ValueError("Could not interpret your input as an integer")
        return num
    
    # Make sure it's positive
    if (val < 0):
        logger.error(f"Input {num} is not positive.")
        raise ValueError(num, ' is not positive.')
    
    return val

# For a given integer n, print out the first n Fibonacci numbers
def fibList(num):
    try:
        num = ensure_positive_int(num)
    except ValueError:
        logger.error("Please enter a positive integer for the number of Fibonacci numbers to generate.")
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
        logger.error(f"Invalid input: {num}. It should be a positive integer.")
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
        logger.error("Zero not valid. Indexing is such that 1st Fibonacci number is 0, 2nd is 1, etc.")
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


import os.path
import distutils.util

NUMBER_OF_BYTES = 16384   # 4 bytes = 32 bit, 8 bytes = 64 bit, ... (fib gets big fast)
MAX_NUMBER_OF_SAVED_DIGITS = 1e5  # If want to store more, will have to increase NUMBER_OF_BYTES
filename = 'savedFibonacciNumbers.bin'

# Stores off the first MAX_NUMBER_OF_DIGITS Fibonacci numbers to a file, to store processing time
def make_saved_Fibonacci_file():
    logger.info("Making a binary file with the first %d Fibonacci numbers." % int(MAX_NUMBER_OF_SAVED_DIGITS))
    # See if file exists already, and warn
    if os.path.isfile(filename):
        logger.warning(f"{filename} already exists with {os.path.getsize(filename)/NUMBER_OF_BYTES} digits.
" \
                       "Do you wish to overwrite? (Y/N):")
        ans = input(prompt)
        overwrite = distutils.util.strtobool(ans)
        if not overwrite:
            logger.info(f"..Exiting without writing over {filename}..")
            return

    savedList = fibList(MAX_NUMBER_OF_SAVED_DIGITS)
    
    # Write binary data to a file
    with open(filename, 'wb') as f:
        for num in savedList:
            f.write(num.to_bytes(NUMBER_OF_BYTES, byteorder='big', signed=False))

# Gets the nth Fibonacci number from a binary file containing all the previously calculated digits.
# Storing the digits as binary lets one seek immediately to the needed number, instead of calculating
# all the number previous.
def get_nth_saved_Fibonacci_number(nth):
    # Correct for index starting at 0 & make sure still positive
    index = ensure_positive_int(nth - 1)
    
    # Make saved list if none exists
    if not os.path.isfile(filename):
        logger.error("Could not find a binary file containing Fibonacci numbers.")
        make_saved_Fibonacci_file()
        return -1

    size = int(os.path.getsize(filename)/NUMBER_OF_BYTES)
    if index >= size:
        msg = str(nth) + " exceeds the number of saved Fibonacci numbers (" + str(size) + ")."
        logger.error(msg)
        return -1
    
    # Read the binary file starting at nth position
    with open(filename, 'rb') as f:
        f.seek(index*NUMBER_OF_BYTES)  # Go to location of nth 4 byte Fibonacci number
        digit = f.read(NUMBER_OF_BYTES)
    
    # Convert binary to integer and return the result
    return int.from_bytes(digit, byteorder='big')

# Nudges a non-fibonacci number to the closest Fibonacci number
# Does a binary search to find lower bound, then chooses nearest Fibonacci number
def nearest_saved_fib(input):
    return get_nth_saved_Fibonacci_number(nearest_saved_fib_index(input))

# Finds index of nearest fib num. Rounds down if tie.
def nearest_saved_fib_index(input):
    numbers_in_file = os.path.getsize(filename)/NUMBER_OF_BYTES

    # Set-up for binary search
    left_index = 1
    right_index = numbers_in_file
    left_fib  = get_nth_saved_Fibonacci_number(left_index)
    right_fib = get_nth_saved_Fibonacci_number(right_index)
    
    # Check input
    if input < 0:
        logger.error("All the Fibonacci numbers are positive. Please enter a positive value.")
        return -1
    if input > right_fib:
        logger.error(f"Input {input} exceeds highest saved Fibonacci number.")
        return -1

    # Binary search to get lower bound for nth Fibonacci number
    while (left_fib < right_fib):
        # Get midpoint
        middle_index = math.floor(left_index + (right_index - left_index) / 2)
        
        # Replace midpoint as appropriate
        if (get_nth_saved_Fibonacci_number(middle_index) < input):
            left_index = middle_index + 1
            left_fib = get_nth_saved_Fibonacci_number(left_index)
        else:
            right_index = middle_index
            right_fib = get_nth_saved_Fibonacci_number(right_index)
    # assert: left_index is now 1 (unchanged), OR 1 past the lower bound for input's index.
    if left_index != 1:
        left_index -= 1
    left_fib = get_nth_saved_Fibonacci_number(left_index)
    right_index = left_index + 1
    right_fib = get_nth_saved_Fibonacci_number(right_index)

    # Choose nearest Fibonacci number
    if ((right_fib - input) < (input - left_fib)):   # picks closest fib, rounds down if equidistant
        output = right_index
    else:
        output = left_index

    return output
