from __future__ import print_function

# Author: Alexandre Gramfort <alexandre.gramfort@inria.fr>
# License: BSD 3 clause

from sklearn import linear_model

import datetime
import numpy as np
import pylab as pl
import scipy
from matplotlib.finance import quotes_historical_yahoo
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import matplotlib.pyplot as plt
def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

print(__doc__)

###############################################################################
# Downloading the data
date1 = datetime.date(1995, 1, 1)  # start date
date2 = datetime.date(2012, 1, 6)  # end date

# for stock in stocks
# get goog quotes from yahoo finance
goog_quotes = quotes_historical_yahoo("GOOG", date1, date2)
if len(goog_quotes) == 0:
    raise SystemExit

# unpack goog quotes
goog_dates = np.array([q[0] for q in goog_quotes], dtype=int)
goog_close_v = np.array([q[2] for q in goog_quotes])
goog_volume = np.array([q[5] for q in goog_quotes])[1:]

# regression tree plot
X = goog_dates[1:151]
y = goog_close_v[1:151]

x = [[i] for i in X] # for use with scipy regession and svm
###############################################################################
# Generate sample data
n_samples_train, end_test_index = 75, 150
#np.random.seed(0)
#coef = np.random.randn(n_features)
#coef[50:] = 0.0  # only the top 10 features are impacting the model
#X = np.random.randn(n_samples_train + n_samples_test, n_features)
#y = np.dot(X, coef)

# Split train and test data
X_train, X_test = X[:n_samples_train], X[n_samples_train : end_test_index]
y_train, y_test = y[:n_samples_train], y[n_samples_train : end_test_index]
##############################################################################
# Compute train and test errors

# Naive
y_last_train = y_train[len(y_train)-1] #naively take the last y as our model
y_last_train_predictions = [y_last_train] * n_samples_train
last_train_error = rmse(y_last_train_predictions, y_test)
print("RMSE Naive: "+str(last_train_error))

# Linear extrapolation = (y2-y1)/(x2-x1)
m = (y_train[len(y_train)-1] - y_train[0]) / (X_train[len(X_train)-1] - X_train[0])
b = y_train[0] - m*X_train[0]
y_linear_predictions = m * X_test + b
linear_error = rmse(y_linear_predictions, y_test)
print("RMSE linear extrapolation: "+str(linear_error))

# Linear regression 
clf = linear_model.LinearRegression()
clf.fit(x,y)
y_regression = clf.coef_ * X_test + clf.intercept_
regression_error = rmse(y_regression, y_test)
print("RMSE linear regression: "+str(regression_error))

# SVM
from sklearn import svm
svm_model = svm.LinearSVC()
svm_model.fit(x,y)
y_svm = svm_model.predict(y_test)
print(i for i in y_svm)

###############################################################################
# Plot results functions

pl.figure()
pl.scatter(X, y, c="k", label="data")
pl.plot(X_test, y_linear_predictions, c="g", label="linear predictions", linewidth=2)
pl.plot(X_test, y_last_train_predictions, c="r", label="last training example", linewidth=2)
pl.plot(X_test, y_regression, c="b", label="linear regression", linewidth=2)
pl.xlabel("data")
pl.ylabel("target")
pl.title("Naive Model")
pl.legend()
pl.show()