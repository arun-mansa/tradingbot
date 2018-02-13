"""Module for IQ Option API TBH pattern."""

from base import Base
import logging

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

            if candles.second_candle.is_spinning_top:
                logger.info("Spinning top")

            if candles.first_candle.candle_close < lw[25] and height[25] > 399:
                if candles.first_candle.candle_type == "red" and candles.second_candle.candle_type == "green":
                    if candles.second_candle.candle_height >= (candles.first_candle.candle_height / 2):
                        logger.info("Lower Band:'%f', First candle close: '%f'.", lw[25], candles.first_candle.candle_close)
                        return True

    def put(self):
        """Method to check put pattern."""
        logger = logging.getLogger("__main__")
        candles = self.candles

        if hasattr(candles, 'first_candle'):
            up, lw, height = self.bolinger_bands(candles=candles)

            if candles.first_candle.candle_close > up[25] and height[25] > 399:
                if candles.first_candle.candle_type == "green" and candles.second_candle.candle_type == "red":
                    if candles.second_candle.candle_height >= (candles.first_candle.candle_height / 2):
                        logger.info("High Band:'%f', First candle close: '%f'.", up[25], candles.first_candle.candle_close)
                        return True
