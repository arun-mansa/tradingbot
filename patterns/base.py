"""Module for IQ Option API base pattern."""
import time
import pandas as pd
import numpy as np

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
        if (not self.api.is_successful) or self.api.timesync.server_datetime.second == 0:
            self.api.getcandles(self.active, 60, 28)
            self.api.is_successful = True
            time.sleep(0.5)
            return self.api.candles

    def rsi(self, candles, period=14):
        """Property to RSI on fetched candels."""

        if hasattr(candles, 'candles_array'):
            candel_array = candles.candles_array
            prices = pd.Series([candle.candle_close for candle in candel_array])
            delta = prices.diff()

            d_up, d_down = delta.copy(), delta.copy()
            d_up[d_up < 0] = 0
            d_down[d_down > 0] = 0

            rol_up = pd.rolling_mean(d_up, period)
            rol_down = pd.rolling_mean(d_down, period).abs()

            relativestrength = rol_up / rol_down
            rsi = 100.0 - (100.0 / (1.0 + relativestrength))
            
            return rsi

    def call(self):
        """Method to check call pattern."""
        pass

    def put(self):
        """Method to check put pattern."""
        pass
