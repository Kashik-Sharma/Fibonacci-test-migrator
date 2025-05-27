from flask import render_template
from app import app
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
@app.route('/index')
def index():
    logging.info("Accessed index page.")
    return render_template('index.html', title="Home")

@app.route('/test_script.html')
def test_script():
    logging.info("Accessed test script page.")
    return render_template('test_script.html')

@app.route('/fib/')
def fib_usage():
    logging.info("Accessed Fibonacci usage page.")
    return render_template('usage.html')

@app.route('/fib/<string:argument>')
def myFib(argument):
    logging.info("Accessed Fibonacci calculation for argument: %s", argument)
    TRUNCATE_AFTER_THIS_MANY = int(1e4)
    try:
        number = int(float(argument))
    except ValueError:
        message = f"Could not interpret {argument} as an integer. Please try again."
        logging.warning("Invalid input: %s", argument)
        return render_template('usage.html', msg=message)
    if number < 0:
        message = f"Invalid input: {number} must be a positive integer."
        logging.warning("Negative input provided: %d", number)
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
                message = f"Truncated output after {TRUNCATE_AFTER_THIS_MANY} numbers."
            i = 2
            while i <= num - 1:
                fibNumbers.append(fibNumbers[i - 2] + fibNumbers[i - 1])
                i += 1
        return fibNumbers, message

    fibs = fibList(number)
    logging.info("Generated Fibonacci sequence up to: %d", number)
    return render_template('output.html', num=number, list=fibs[0], msg=fibs[1])