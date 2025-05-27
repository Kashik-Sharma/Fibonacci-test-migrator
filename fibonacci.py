# J. Pocahontas Olson   June 2016
# Fibonacci generator

import fibonacci_module as fb         # Custom module made for this project
import math                           # Math functions (log, pow, sqrt, etc.)
import matplotlib.pyplot as plt       # Plotting
import pylab
from scipy.optimize import curve_fit  # Curve fitting
from sklearn.metrics import mean_squared_error  # Error of fit
from distutils.util import strtobool  # Translates user answer to Yes/No question to bool
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

FIRSTPOINTS  = int(100)
PREDICTPOINT = int(500)

# Introduction to user
logging.info("Welcome!")

###############################
### (1.)  Graph first 100 (FIRSTPOINTS) Fibonacci numbers
###############################
y = fb.fibList(FIRSTPOINTS)
x = list(range(1,FIRSTPOINTS+1))  # Adjusts for index starting at 0
logging.info("Would you like to see a graph of the first %d Fibonacci numbers?", FIRSTPOINTS)
showit = strtobool(input("  [Figure 1]  Y/N: "))
if showit:
    plt.figure(1)
    plt.plot(x, y)
    plt.xlabel('n^th Fibonacci number')
    plt.ylabel('Fibonacci number')
    plt.title('First ' + str(FIRSTPOINTS) + ' Fibonacci numbers')
    #plt.yscale('log')  # Uncomment to see log graph
    pylab.show(block=False)
logging.info("From Figure 1, we can see that the Fibonacci numbers grow exponentially.")

##############################
## (2.) Let's try to fit the data!
##############################
logging.info("Our first thought would be to fit an exponential to this data.")
logging.info("However, because of the large numbers involved, it's better to fit")
logging.info("a line to the log of the Fibonacci numbers.")
# Generate the log values of the true Fibonacci numbers
log_x = x[1:]  # Ignore first fibonacci number b/c log(0) is undefined
log_y = [math.log(fibNum) for fibNum in y[1:]]
# Define a line to fit the log of the Fib numbers
def fitLogPrediction(x, m, b):    # x is input, and m and b are the slope and y-intercept of the line, respectively
    return m * x + b
# Function to convert from the fit of log scale, to actual prediction of fibonacci number (rounds to nearest int)
def fitFibPrediction(x, m, b):
    return round(math.exp(fitLogPrediction(x, m, b)))
# Find 500th (PREDICTPOINT) Fibonacci number as well
predictList = fb.fibList(PREDICTPOINT)

# Fit the line, plot it in red, predict 500th point
popt, pcov = curve_fit(fitLogPrediction, log_x, log_y)   # Finds slope and y-intercept that best fit
fit_y = [fitLogPrediction(nFib,popt[0],popt[1]) for nFib in log_x]  # Makes the line that fits
fitlog500prediction = fitLogPrediction(PREDICTPOINT,popt[0],popt[1])
actual500num = predictList[PREDICTPOINT-1]
# Find error bars for extrapolated predictions
logerror = math.sqrt(mean_squared_error(log_y, fit_y))*math.sqrt(FIRSTPOINTS)
lower500bound = math.exp(fitlog500prediction-logerror)
upper500bound = math.exp(fitlog500prediction+logerror)
logging.info("Fitting a line to the data, the best fit has slope %f and y-intercept %f", popt[0], popt[1])

# For large n, the slope approaches phi = (1+sqrt(5))/2.  Let's see what we got.
logging.info("We can compare this to the theoretical limit (applicable for large n),")
logging.info("which should yield the golden ratio.")
logging.info("Compare the fit's prediction: %f", math.exp(popt[0]))
logging.info("to the golden ratio phi: %f", fb.phi)
logging.info("So after using only %d Fibonacci numbers, the fit behavior differs from", FIRSTPOINTS)
logging.info("the theoretical limit by %f %%", 100*(1- math.exp(popt[0])/fb.phi))

logging.info("Would you like to see a graph of the line we fit to the first %d Fibonacci numbers, on a log scale?", FIRSTPOINTS)
showit = strtobool(input("  [Figure 2]  Y/N: "))
if showit:
    plt.figure(2)
    plt.subplot(211)
    plt.plot(log_x, log_y, "bs")  # Log values in blue squares
    plt.plot(log_x, fit_y, 'r-')  # Fit in red dashes
    plt.xlabel('n^th Fibonacci number')
    plt.ylabel('Log of Fibonacci number')
    plt.title('Fitted prediction of Fibonacci numbers, on log scale')
    plt.subplots_adjust(hspace=0.5)
    plt.subplot(212)
    plt.plot(log_x + [PREDICTPOINT], log_y + [math.log(actual500num)], "bs")  # Log values in blue squares
    plt.plot(log_x + [PREDICTPOINT], fit_y + [fitlog500prediction], 'r-')  # Fit in red dashes
    plt.xlabel('n^th Fibonacci number')
    plt.ylabel('Log of Fibonacci number')
    plt.title('Same graph, extrapolated to predict 500th Fibonacci number')
    pylab.show(block=False)
logging.info("From Figure 2, we can see that the fit seems to match the first %d Fibonacci numbers well,", FIRSTPOINTS)
logging.info("and extrapolating the fit to predict the %d th Fibonacci number seems pretty good also.", PREDICTPOINT)
logging.info("In fact, the fit predicts the %d th Fibonacci number to be %12E", PREDICTPOINT, math.exp(fitlog500prediction))
logging.info("within [%12E, %12E]. The actual value, %12E, is within these bounds.", lower500bound, upper500bound, actual500num)

logging.info("Now let us investigate how much the fit is off by.")

#############################
# (3.) Let's see how well our fit did
#############################
fit_differences = [y[nFib-1] - fitFibPrediction(nFib-1,popt[0],popt[1]) for nFib in log_x]
fit_percent_differences = [(y[nFib-1] - fitFibPrediction(nFib-1,popt[0],popt[1]))/y[nFib-1] for nFib in log_x]

logging.info("We have calculated the fit's prediction of the first %d Fibonacci numbers,", FIRSTPOINTS)
logging.info("to compare to the actual Fibonacci numbers.")