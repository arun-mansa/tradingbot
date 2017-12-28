"""Module for IQ Option API DBLHC pattern."""

import logging
from base import Base

class DBLHC(Base):
    """Class for DBLHC pattern."""
    # pylint: disable=too-few-public-methods

    def __init__(self, api, active):
        """
        :param api: The instance of
            :class:`IQOptionAPI <iqoptionapi.api.IQOptionAPI>`.
        """
        super(DBLHC, self).__init__(api, active)
        self.name = "DBLHC"

    def call(self):
        """Method to check call pattern."""
        logger = logging.getLogger("__main__")
        candles = self.candles

        if hasattr(candles, 'first_candle') and hasattr(candles, 'second_candle'):
            up, lw = self.bolinger_bands(candles=candles)

            if candles.first_candle.candle_low <= lw[26]:
                if candles.first_candle.candle_low == candles.second_candle.candle_low:
                    if candles.second_candle.candle_close > candles.first_candle.candle_low:
                        logger.info("Lower Band:'%f', First candle low: '%f'.", lw[26], candles.first_candle.candle_low)
                        logger.info("First candle low:'%f', Second candle low: '%f'.", candles.first_candle.candle_low, candles.second_candle.candle_low)
                        logger.info("Second candle close:'%f', First candle low: '%f'.", candles.second_candle.candle_close, candles.first_candle.candle_low)
                        return True
