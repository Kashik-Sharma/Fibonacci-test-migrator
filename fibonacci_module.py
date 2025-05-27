# J. Pocahontas Olson  June 2016
# Module containing function definitions relating to the Fibonacci numbers

import math
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# A check to ensure that inputs are positive integers, which most of these functions require
def ensure_positive_int(num):
    # Make sure it's an integer
    try:
        val = int(num)
    except ValueError:
        logging.error("Could not interpret input as an integer")
        raise ValueError("Could not interpret your input as an integer")
        return num
    
    # Make sure it's positive
    if (val < 0):
        logging.error(f"{num} is not positive.")
        raise ValueError(num, ' is not positive.')
    
    return val

# For a given integer n, log out the first n Fibonacci numbers
def fibList(num):
    try:
        num = ensure_positive_int(num)
    except ValueError:
        logging.warning("Please enter a positive integer for the number of Fibonacci numbers to generate.")
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
        raise ValueError('Invalid input. ', num, ' should be a positive integer.')
    
    return fibNumbers

#### Theoretical Predictions ####
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
    if int(root + 0.5) ** 2 == integer:  # int() floors it, adding .5 so 2.999 & 3.001 map to 3
        return True
    else:
        return False

# A function to determine if a number is a fibonacci number
# For more info, refer to https://en.wikipedia.org/wiki/Fibonacci_number#Recognizing_Fibonacci_numbers
def is_fibonacci(integer):
    integer = ensure_positive_int(integer)
    return (is_square(5 * math.pow(integer, 2) + 4) or is_square(5 * math.pow(integer, 2) - 4))

# Binet's formula to find n for a given Fibonacci number
def n_Binet(input):
    input = ensure_positive_int(input)
    if input == 0:
        return (1, 1)  # 0 is the first Fibonacci number
    numerator_plus = input * math.sqrt(5) + math.sqrt(5 * math.pow(input, 2) + 4)
    numerator_minus = input * math.sqrt(5) + math.sqrt(5 * math.pow(input, 2) - 4)
    n_plus = math.log(numerator_plus / 2, phi)
    n_minus = math.log(numerator_minus / 2, phi)

    if is_square(numerator_plus):
        return (n_plus, n_plus)
    elif is_square(numerator_minus):
        return (n_minus, n_minus)
    else:
        return (n_plus, n_minus)

# Binet's formula to find the nth Fibonacci number
def f_Binet(nth):
    nth = ensure_positive_int(nth)
    if nth == 0:
        raise ValueError("Zero not valid. Indexing is such that 1st Fib num is 0, 2nd is 1, etc.")
    if nth == 1:
        return 0  # 0 is the first Fibonacci number
    nth -= 1
    
    return round((math.pow(phi, nth) - math.pow(psi, nth)) / math.sqrt(5))

# Nudges a non-fibonacci number to the closest fibonacci number
def nearest_Binet_fib(input):
    input = ensure_positive_int(input)
    if input == 0:
        return 0  # 0 is the first Fibonacci number
    
    (n_plus, n_minus) = n_Binet(input)
    if round(n_plus) == round(n_minus):
        return f_Binet(round(n_plus))
    else:
        fib_plus = f_Binet(round(n_plus))
        fib_minus = f_Binet(round(n_minus))
        if abs(fib_plus - input) < abs(fib_minus - input):
            return fib_plus
        else:
            return fib_minus

#### Saving Values ####
# Save values of Fibonacci numbers ahead of time

import os.path
import distutils.util

NUMBER_OF_BYTES = 16384  # Fibonacci grows fast
MAX_NUMBER_OF_SAVED_DIGITS = int(1e5)
filename = 'savedFibonacciNumbers.bin'

# Save Fibonacci numbers to a binary file for efficiency
def make_saved_Fibonacci_file():
    logging.info("Creating binary file with first %d Fibonacci numbers.", MAX_NUMBER_OF_SAVED_DIGITS)
    if os.path.isfile(filename):
        logging.warning("File %s already exists.", filename)
        ans = input("Overwrite?: (Y/N) ")
        if not distutils.util.strtobool(ans):
            logging.info("Exiting without overwriting %s", filename)
            return

    savedList = fibList(MAX_NUMBER_OF_SAVED_DIGITS)
    # Write binary data
    with open(filename, 'wb') as f:
        for num in savedList:
            f.write(num.to_bytes(NUMBER_OF_BYTES, byteorder='big', signed=False))

# Retrieve nth Fibonacci number from binary file
def get_nth_saved_Fibonacci_number(nth):
    index = ensure_positive_int(nth - 1)
    if not os.path.isfile(filename):
        ans = input("Create new Fibonacci file? (Y/N) ")
        if distutils.util.strtobool(ans):
            make_saved_Fibonacci_file()
        else:
            raise IOError("File not found.")

    size = int(os.path.getsize(filename) / NUMBER_OF_BYTES)
    if index >= size:
        raise ValueError(f"{nth} exceeds saved range in {filename}.")

    with open(filename, 'rb') as f:
        f.seek(index * NUMBER_OF_BYTES)
        digit = f.read(NUMBER_OF_BYTES)
    return int.from_bytes(digit, byteorder='big')

# Helper to find nearest Fibonacci number from binary file
def nearest_saved_fib(input):
    return get_nth_saved_Fibonacci_number(nearest_saved_fib_index(input))

# Binary search for minimum distance fibonacci index
def nearest_saved_fib_index(input):
    numbers_in_file = int(os.path.getsize(filename) / NUMBER_OF_BYTES)
    left_index = 1
    right_index = numbers_in_file

    left_fib = get_nth_saved_Fibonacci_number(left_index)
    right_fib = get_nth_saved_Fibonacci_number(right_index)

    if input < 0:
        logging.error("Negative value encountered: %d", input)
        raise ValueError("All Fibonacci numbers are positive.")
    if input > right_fib:
        logging.error("Value %d exceeds maximum saved Fibonacci number.", input)
        raise ValueError(input)

    while left_fib < right_fib:
        middle_index = math.floor(left_index + (right_index - left_index) / 2)

        if get_nth_saved_Fibonacci_number(middle_index) < input:
            left_index = middle_index + 1
            left_fib = get_nth_saved_Fibonacci_number(left_index)
        else:
            right_index = middle_index
            right_fib = get_nth_saved_Fibonacci_number(right_index)

    if left_index != 1:
        left_index -= 1
    left_fib = get_nth_saved_Fibonacci_number(left_index)
    right_index = left_index + 1
    right_fib = get_nth_saved_Fibonacci_number(right_index)

    output = right_index if (right_fib - input) < (input - left_fib) else left_index
    logging.info("Nearest saved Fibonacci number index for input %d is %d", input, output)
    return output