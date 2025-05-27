import fibonacci_module as fb
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("Testing Fibonacci functionalities.")

####    Tests for Fibonacci Numbers    ####
logger.info("Sample inputs for list of Fibonacci numbers")
logger.info("  n=0:   %s", fb.fibList(0))
logger.info("  n=1:   %s", fb.fibList(1))
logger.info("  n=2:   %s", fb.fibList(2))
logger.info("  n=3.2: %s", fb.fibList(3.2))
logger.info("  n=4.9: %s", fb.fibList(4.9))
logger.info("  n=5:   %s", fb.fibList(5))
logger.info("  n=15:  %s", fb.fibList(15))
logger.info("  n=100: %s", fb.fibList(100))

logger.info("
Intentionally using invalid inputs")
logger.info("  n=-1: %s", fb.fibList(-1))
logger.info("  n=foo: %s", fb.fibList("foo"))

####    Tests for Square Numbers    ####
logger.info("
Tests for is_square function:")
testList = [0, 1, 2, 3, 4, +8, +9, 16, 25.0, 120.9999999, 1e4]
logger.info("  Number   Perfect Square?")
for val in testList:
    logger.info("  %s       %s", val, fb.is_square(val))
## Stuff that should error
#logger.info("  -9", fb.is_square(-9))
#logger.info(" foo", fb.is_square("foo"))

####    Tests for Is_Fibonacci    ####
logger.info("
Tests for is_fibonacci function:")
testList = [0, 1, 2, 3, 4, 5, 12, 13, 42, 218922995834555169026]
testList = [(0, "Y"), (1, "Y"), (2, "Y"), (3, "Y"), (4, "N"), (5, "Y"), (12, "N"), (13, "Y"), (42, "N"), (144, "Y"), (63245986,"Y"), (102334155, "Y"), (218922995834555169026, "Y")]
logger.info("  Number   Fibonacci?   Expected")
for val in testList:
    logger.info("  %s       %s       %s", val[0], fb.is_fibonacci(val[0]), val[1])
    if (val[0] == 63245986):
        logger.info("     (Now exceeds numerical precision)")

####    Tests for Binet's Formula    ####
logger.info("
Tests for Binet's Formula:")
logger.info("  Number   Fibonacci?   Nearest n   Nearest fib   n range")
for val in testList:
    nrange = fb.n_Binet(val[0])
    logger.info("  %s       %s       %s       %s       %s", val[0], val[1], round(nrange[0]), fb.nearest_Binet_fib(val[0]), nrange)

####    Tests for Saving off Fibonacci Numbers   ###
if not fb.os.path.isfile(fb.filename):
    fb.make_saved_Fibonacci_file()

logger.info("
Tests for Saving off Fibonacci Numbers:")
saved = [fb.get_nth_saved_Fibonacci_number(n) for n in range(1,11)]
logger.info("  first 10 saved numbers: %s", saved)
for n in [12, 20, 40, 80, 98, 99, 100, 101, 200, 1000, 5000]:
    logger.info("   %sth fib: %s", n, fb.get_nth_saved_Fibonacci_number(n))