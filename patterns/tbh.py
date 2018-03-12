"""Module for IQ Option API TBH pattern."""

from base import Base
import logging
import csv
import pickle

class TBH(Base):
    """Class for TBH pattern."""

    def __init__(self, api, active):
        """
        :param api: The instance of
            :class:`IQOptionAPI <iqoptionapi.api.IQOptionAPI>`.
        """
        super(TBH, self).__init__(api, active)
        self.name = "TBH"

    def call(self):
        """Method to check call pattern."""
        logger = logging.getLogger("__main__")
        candles = self.candles

        if hasattr(candles, 'first_candle'):
            up, lw, height = self.bolinger_bands(candles=candles)
            rsi14 = self.rsi(candles=candles)
            K, D = self.stoc_occilator(candles=candles)
            aroon_up, aroon_down = self.aroon(candles=candles, period=14)

            # loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
            # predicted_price = loaded_model.predict([[up[26] - candles.first_candle.candle_close, lw[26] - candles.first_candle.candle_close, candles.first_candle.candle_height - candles.second_candle.candle_height, rsi14[28], K[28], D[28], aroon_up[29], aroon_down[29]]])
            logger.info("First candle close:'%i'", candles.first_candle.candle_close)
            logger.info("AR Up: '%i', AR Down:'%i'", aroon_up[29], aroon_down[29])

            if candles.first_candle.candle_close <= lw[26] and height[26] > 499:
                if candles.first_candle.candle_type == "red" and candles.second_candle.candle_type == "green":
                    if candles.second_candle.candle_height >= (candles.first_candle.candle_height / 2):
                        if aroon_down[29] - aroon_up[29] < 50:
                            logger.info("Lower Band:'%i', First candle close: '%i'.", lw[26], candles.first_candle.candle_close)
                            return True

    def put(self):
        """Method to check put pattern."""
        logger = logging.getLogger("__main__")
        candles = self.candles

        if hasattr(candles, 'first_candle'):
            up, lw, height = self.bolinger_bands(candles=candles)
            rsi14 = self.rsi(candles=candles)
            K, D = self.stoc_occilator(candles=candles)
            aroon_up, aroon_down = self.aroon(candles=candles, period=14)

            # loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
            # predicted_price = loaded_model.predict([[up[26] - candles.first_candle.candle_close, lw[26] - candles.first_candle.candle_close, candles.first_candle.candle_height - candles.second_candle.candle_height, rsi14[28], K[28], D[28], aroon_up[29], aroon_down[29]]])
            
            if candles.first_candle.candle_close >= up[26] and height[26] > 499:
                if candles.first_candle.candle_type == "green" and candles.second_candle.candle_type == "red":
                    if candles.second_candle.candle_height >= (candles.first_candle.candle_height / 2):
                        if aroon_up[29] - aroon_down[29] < 50:
                            logger.info("High Band:'%i', First candle close: '%i'.", up[26], candles.first_candle.candle_close)
                            return True
