"""Module for IQ Option API base pattern."""
import time
import pandas as pd
import numpy as np
import logging

class Base(object):
    """Class for IQ Option API base pattern."""

    def __init__(self, api, active):
        """
        :param api: The instance of
            :class:`IQOptionAPI <iqoptionapi.api.IQOptionAPI>`.
        """
        self.api = api
        self.active = active

    @property
    def candles(self):
        """Property to get candles."""
        if  self.api.timesync.server_datetime.second == 0:
            self.api.getcandles(self.active, 60, 28)
            time.sleep(0.5)
            return self.api.candles

    def rsi(self, candles, period=14):
        """Method to get RSI on fetched candels."""
        logger = logging.getLogger("__main__")
        if hasattr(candles, 'candles_array'):
            candel_array = candles.candles_array
            prices = pd.Series([candle.candle_close for candle in candel_array])
            delta = prices.diff()

            d_up, d_down = delta.copy(), delta.copy()
            d_up[d_up < 0] = 0
            d_down[d_down > 0] = 0

            rol_up = d_up.rolling(window=period).mean()
            rol_down = d_down.rolling(window=period).mean().abs()

            relativestrength = rol_up / rol_down
            rsi = 100.0 - (100.0 / (1.0 + relativestrength))
            logger.info("RSI for first candle '%f'.", rsi[26])
            return rsi

    def bolinger_bands(self, candles, period=14, num_of_std=2):
        """Method to get BB on fetched candels."""
        logger = logging.getLogger("__main__")
        if hasattr(candles, 'candles_array'):
            candel_array = candles.candles_array
            prices = pd.Series([candle.candle_close for candle in candel_array])

            rolling_mean = prices.rolling(window=period).mean()
            rolling_std  = prices.rolling(window=period).std()
            upper_band = rolling_mean + (rolling_std*num_of_std)
            lower_band = rolling_mean - (rolling_std*num_of_std)

            # logger.info("Upper Band:'%f', Lower Band: '%f'.", upper_band[26], lower_band[26])
            return upper_band, lower_band

    def call(self):
        """Method to check call pattern."""
        pass

    def put(self):
        """Method to check put pattern."""
        pass
