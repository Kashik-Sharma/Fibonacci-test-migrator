import fibonacci_module as fb
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Starting tests for Fibonacci Numbers")

####    Tests for Fibonacci Numbers    ####
logging.info("Sample inputs for list of Fibonacci numbers")
logging.info("n=0: %s", fb.fibList(0))
logging.info("n=1: %s", fb.fibList(1))
logging.info("n=2: %s", fb.fibList(2))
logging.info("n=3.2: %s", fb.fibList(3.2))
logging.info("n=4.9: %s", fb.fibList(4.9))
logging.info("n=5: %s", fb.fibList(5))
logging.info("n=15: %s", fb.fibList(15))
logging.info("n=100: %s", fb.fibList(100))

logging.info("Intentionally using invalid inputs")
logging.info("n=-1: %s", fb.fibList(-1))
logging.info("n=foo: %s", fb.fibList("foo"))

####    Tests for Square Numbers    ####
logging.info("Tests for is_square function:")
testList = [0, 1, 2, 3, 4, +8, +9, 16, 25.0, 120.9999999, 1e4]
logging.info("Number   Perfect Square?")
for val in testList:
    logging.info("%s   %s", val, fb.is_square(val))

####    Tests for Is_Fibonacci    ####
logging.info("Tests for is_fibonacci function:")
testList = [0, 1, 2, 3, 4, 5, 12, 13, 42, 218922995834555169026]
logging.info("Number   Fibonacci? Expected")
for val in testList:
    logging.info("%s  %s", val, fb.is_fibonacci(val))

####    Tests for Saving off Fibonacci Numbers    ####
logging.info("Testing saved Fibonacci Numbers:")
if not fb.os.path.isfile(fb.filename):
    fb.make_saved_Fibonacci_file()

saved = [fb.get_nth_saved_Fibonacci_number(n) for n in range(1,11)]
logging.info("First 10 saved numbers: %s", saved)
for n in [12, 20, 40, 80, 98, 99, 100, 101, 200, 1000, 5000]:
    logging.info("%s th fib: %s", n, fb.get_nth_saved_Fibonacci_number(n))