import logging
from flask import render_template
from app import app

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route('/')
@app.route('/index')
def index():
    logger.info("Rendering index page.")
    return render_template('index.html', title="Home")

@app.route('/test_script.html')
def test_script():
    logger.info("Rendering test_script page.")
    return render_template('test_script.html')

@app.route('/fib/')
def fib_usage():
    logger.info("Rendering Fibonacci usage page.")
    return render_template('usage.html')

@app.route('/fib/<string:argument>')
def myFib(argument):
    TRUNCATE_AFTER_THIS_MANY = 1e4

    try:
        number = int(float(argument))
        logger.info("Generating Fibonacci list for number: %d", number)
    except ValueError:
        logger.error("Could not interpret input as an integer: %s", argument)
        message = "Could not interpret " + argument + " as an integer. Please enter a positive integer."
        return render_template('usage.html', msg=message)
    
    if number < 0:
        message = "Invalid input. " + str(number) + " must be a positive integer."
        logger.error(message)
        return render_template('usage.html', msg=message)

    def fibList(num):
        fibNumbers = []
        message = ""
        if num >= 1:
            fibNumbers.append(0)
        if num >= 2:
            fibNumbers.append(1)
        if num > 2:
            if num > TRUNCATE_AFTER_THIS_MANY:
                num = TRUNCATE_AFTER_THIS_MANY
                message = "Results truncated at " + str(int(TRUNCATE_AFTER_THIS_MANY)) + " numbers."
            i = 2
            while i <= num - 1:
                fibNumbers.append(fibNumbers[i - 2] + fibNumbers[i - 1])
                i += 1
        return (fibNumbers, message)

    result, msg = fibList(number)
    logger.info("Generated Fibonacci list with %d numbers.", len(result))
    return render_template('output.html', num=number, list=result, msg=msg)