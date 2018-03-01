# Save Model Using Pickle
import csv
import time
import pickle
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import iqoptionapi.constants as api_constants

from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import ElasticNet
from sklearn.svm import SVR
from sklearn.svm import LinearSVC
from iqoptionapi.api import IQOptionAPI
from config import parse_config


class Learner(object):
    """Class for ML."""

    def __init__(self, api, active):
        self.api = api
        self.active = api_constants.ACTIVES[active]


    def fetch_candles(self):
        """Methond to fetch candles form IQOptions Websocket api"""
        while not (self.active in self.api.activeCandles):
            self.api.getcandles(self.active, 60, 1000)
            time.sleep(3)

        if self.active in self.api.activeCandles:
            return self.api.activeCandles[self.active]
        else:
            return False

    def rsi(self, candles, period=14):
        """Method to get RSI on fetched candels."""
        if hasattr(candles, 'candles_array'):
            candel_array = candles.candles_array
            prices = pd.Series(
                [candle.candle_close for candle in candel_array])
            delta = prices.diff()

            d_up, d_down = delta.copy(), delta.copy()
            d_up[d_up < 0] = 0
            d_down[d_down > 0] = 0

            rol_up = d_up.rolling(window=period).mean()
            rol_down = d_down.rolling(window=period).mean().abs()

            relativestrength = rol_up / rol_down
            rsi = 100.0 - (100.0 / (1.0 + relativestrength))

            return rsi

    def bolinger_bands(self, candles, period=14, num_of_std=2):
        """Method to get BB on fetched candels."""
        if hasattr(candles, 'candles_array'):
            candel_array = candles.candles_array
            prices = pd.Series([candle.candle_close for candle in candel_array])

            rolling_mean = prices.rolling(window=period).mean()
            rolling_std = prices.rolling(window=period).std()
            upper_band = rolling_mean + (rolling_std*num_of_std)
            lower_band = rolling_mean - (rolling_std*num_of_std)

            return upper_band, lower_band

    def create_csv(self):
        """Method to create csv based on fetched candels."""
        url = "traningData.csv"
        candles = self.fetch_candles()

        if hasattr(candles, 'first_candle'):
            up, lw = self.bolinger_bands(candles=candles)
            rsi7 = self.rsi(candles=candles, period=7)
            rsi14 = self.rsi(candles=candles, period=14)
            rsi28 = self.rsi(candles=candles, period=28)

            candles_array = candles.candles_array
            ofile = open(url, "wb+")
            writer = csv.writer(ofile, quoting=csv.QUOTE_NONE, escapechar='\n')
            for index, candle in enumerate(candles_array):
                if index > 28 and candle.candle_close > 0:
                    if candles_array[index - 2].candle_close < lw[index - 3]:
                        if candles_array[index - 2].candle_type == "red" and candles_array[index - 1].candle_type == "green":
                            if candles_array[index - 1].candle_height >= (candles_array[index - 2].candle_height / 2):
                                category = 1 if candle.candle_type == "green" else -1
                                writer.writerow([candles_array[index - 1].candle_open, candles_array[index - 1].candle_close, rsi7[index - 1], rsi14[index - 1], rsi28[index - 1], up[index - 1], lw[index - 1], category])
                    elif candles_array[index - 2].candle_close > up[index - 3]:
                        if candles_array[index - 2].candle_type == "green" and candles_array[index - 1].candle_type == "red":
                            if candles_array[index - 1].candle_height >= (candles_array[index - 2].candle_height / 2):
                                category = 1 if candle.candle_type == "green" else -1
                                writer.writerow([candles_array[index - 1].candle_open, candles_array[index - 1].candle_close, rsi7[index - 1], rsi14[index - 1], rsi28[index - 1], up[index - 1], lw[index - 1], category])
                    else:
                        writer.writerow([candles_array[index - 1].candle_open, candles_array[index - 1].candle_close, rsi7[index - 1], rsi14[index - 1], rsi28[index - 1], up[index - 1], lw[index - 1], 0])
            ofile.close()

    def save_model(self):
        """Method to save liner regression model."""
        url = "traningData.csv"
        dataframe = read_csv(url)
        array = dataframe.values
        X = array[:, 0:7]
        Y = array[:, 7]
        # model = SVR(kernel= 'rbf', C= 1e3, gamma= 0.1)
        # model = LogisticRegression()
        # model = ElasticNet(random_state=0)
        model = LinearSVC(random_state=0)
        model.fit(X, Y)

        # save the model to disk
        filename = 'finalized_model.sav'
        pickle.dump(model, open(filename, 'wb'))

        return


def create_learner(api, active):
    """Method for create learner.

    :param api: The IQ Option API.
    :param active: The trader active.
    """
    logger = logging.getLogger(__name__)
    logger.info("Create learner for active '%s'.", active)
    return Learner(api, active)

# url = "traningData.csv"
# dataframe = read_csv(url)
# array = dataframe.values
# X = array[:, 0:7]
# Y = array[:, 7]

# test_size = 0.33
# seed = 7
# X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)

# # Fit the model on 33%
# model = LinearSVC(random_state=0)
# model.fit(X_train, Y_train)
# # save the model to disk

# filename ='finalized_model.sav'
# pickle.dump(model, open(filename,'wb'))

# # some time later...

# # load the model from disk
# loaded_model = pickle.load(open(filename,'rb'))
# result = loaded_model.score(X_test, Y_test)
# print(result)