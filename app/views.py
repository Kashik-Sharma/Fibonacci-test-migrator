from flask import render_template
from app import app
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route('/')
@app.route('/index')
def index():
    logger.info("Rendering home page.")
    return render_template('index.html', title="Home")

@app.route('/test_script.html')
def test_script():
    logger.info("Rendering test script page.")
    return render_template('test_script.html')

@app.route('/fib/')
def fib_usage():
    logger.info("Rendering Fibonacci usage page.")
    return render_template('usage.html')

@app.route('/fib/<string:argument>')
def myFib(argument):
    logger.info("Processing Fibonacci request with argument: %s", argument)
    TRUNCATE_AFTER_THIS_MANY = 1e4
    
    # Validate input
    try:
        number = int(float(argument))  # Float handles scientific notation
    except Exception as e:
        message = f"Could not interpret {argument} as an integer. Please enter a positive integer in the URL."
        logger.warning(message)
        return render_template('usage.html', msg=message)

    if number < 0:
        message = f"Invalid input. {number} must be a positive integer. Please try again."
        logger.warning(message)
        return render_template('usage.html', msg=message)
    
    def fibList(num):
        fibNumbers = []
        message = ""
            
        if num >= 1:
            fibNumbers.append(0)
        if num >= 2:
            fibNumbers.append(1)
        if num > 2:  # assert: fibNumbers = [0, 1]
            if num > TRUNCATE_AFTER_THIS_MANY:
                num = TRUNCATE_AFTER_THIS_MANY
                message = f"Truncated output after {int(TRUNCATE_AFTER_THIS_MANY)} numbers."
                logger.info(message)

            i = 2
            while i <= num - 1:  # -1 adjusts for zero-indexing
                fibNumbers.append(fibNumbers[i-2] + fibNumbers[i-1])
                i += 1

        if num < 0:
            message = f"Invalid input. {num} should be a positive integer."
            logger.error(message)
            raise ValueError(message)

        return (fibNumbers, message)

    fibs = fibList(number)
    logger.info("Generated Fibonacci sequence for %d numbers.", number)
    return render_template('output.html', num=number, list=fibs[0], msg=fibs[1])