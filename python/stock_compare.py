from __future__ import print_function

import datetime
import numpy as np
import pylab as pl
from matplotlib.finance import quotes_historical_yahoo_ochl
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import matplotlib.pyplot as plt
#from sklearn.hmm import GaussianHMM

print(__doc__)

###############################################################################
# Downloading the data
date1 = datetime.date(1995, 1, 1)  # start date
date2 = datetime.date(2012, 1, 6)  # end date
stocks = ["YHOO", "GOOG"]
n_stocks = len(stocks)
quotes = {} #empty dictionary
dates = {}
close_values = {}
volumes = {}

for stock in stocks:
	#download quotes
	quotes[stock] = quotes_historical_yahoo_ochl(stock, date1, date2)
	if len(quotes[stock]) == 0:
		raise SystemExit
	#unpack dates, closes and volumes
	dates[stock] = np.array([q[0] for q in quotes[stock]], dtype=int)
	close_values[stock] = np.array([q[2] for q in quotes[stock]])
	volumes = np.array([q[5] for q in quotes[stock]])[1:]

###################################################
#Plotting

fig, (ax0, ax1) = plt.subplots(nrows=n_stocks)

ax0.plot(dates[stocks[0]][1:20], close_values[stocks[0]][1:20])
ax0.set_title(stocks[0])

ax1.plot(dates[stocks[1]][1:20], close_values[stocks[1]][1:20])
ax1.set_title(stocks[1])

# Hide the right and top spines
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
# Only show ticks on the left and bottom spines
ax1.yaxis.set_ticks_position('left')
ax1.xaxis.set_ticks_position('bottom')

# Tweak spacing between subplots to prevent labels from overlapping
plt.subplots_adjust(hspace=0.5)
plt.show()
