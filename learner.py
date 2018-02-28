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
from iqoptionapi.api import IQOptionAPI
from config import parse_config


class Learner(object):
    """Class for ML."""

    def __init__(self, api, active):
        self.api = api
        self.active = api_constants.ACTIVES[active]


    def fetch_candles(self):
        """Methond to fetch candles form IQOptions Websocket api"""
        self.api.getcandles(self.active, 60, 250)

        time.sleep(2)

        return self.api.activeCandles[self.active]

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
            rsi14 = self.rsi(candles=candles)

            candles_array = candles.candles_array
            ofile = open(url, "ab+")
            writer = csv.writer(ofile, quoting=csv.QUOTE_NONE, escapechar='\n')
            for index, candle in enumerate(candles_array):
                if index > 28 and candle.candle_close > 0:
                    writer.writerow([candles_array[index - 1].candle_open, candles_array[index - 1].candle_close, up[index - 1], lw[index - 1], candle.candle_close])
            ofile.close()

    def save_model(self):
        """Method to save liner regression model."""
        url = "traningData.csv"
        dataframe = read_csv(url)
        array = dataframe.values
        X = array[:, 0:4]
        Y = array[:, 4]

        # model = SVR(kernel= 'rbf', C= 1e3, gamma= 0.1)
        # model = LogisticRegression()
        model = ElasticNet(random_state=0)
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
