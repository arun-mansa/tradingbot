# Save Model Using Pickle
import csv
import pickle
import numpy as np
import matplotlib.pyplot as plt

from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from iqoptionapi.api import IQOptionAPI
from config import parse_config

class Learner(object):
    """Calss for IQ Option API trader."""

    def __init__(self, api, active):
        self.api = api
        self.active = active

	def fetch_candles(self):
        """ Methond to fetch candles form IQOptions Websocket api"""
        self.api.getcandles(self.active, 60, 208)

        self.fetched_candles[self.active] = True
        self.fetched_candles['time'] = self.api.timesync.server_datetime

        time.sleep(3)

url = "traningData.csv"

# ofile  = open(url, "ab+")
# writer = csv.writer(ofile, quoting=csv.QUOTE_NONE, escapechar='\n')
# writer.writerow(self.candle_csv_details(candles, rsi, up, lw, height))
# ofile.close()

names = ['open', 'close', 'high', 'low', 'rsi', 'bb_up', 'bb_low', 'type']
dataframe = read_csv(url, names=names)
array = dataframe.values
X = array[:,0:7]
Y = array[:,7]
test_size = 0.33
seed = 7

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)
# Fit the model on 33%
model = LogisticRegression()
model.fit(X_train, Y_train)
# save the model to disk
filename = 'finalized_model.sav'
pickle.dump(model, open(filename, 'wb'))

# some time later...

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.score(X_test, Y_test)
predicted_Y = loaded_model.predict(X_test)
# plt.plot(predicted_Y)
# plt.plot(Y_test)
print(predicted_Y)
print(Y_test)
print(result)
# plt.show()