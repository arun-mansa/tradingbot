"""Module for IQ Option API DBHLC pattern."""

from base import Base
import logging

class DBHLC(Base):
    """Class for DBLHC pattern."""
    # pylint: disable=too-few-public-methods

    def __init__(self, api, active):
        """
        :param api: The instance of
            :class:`IQOptionAPI <iqoptionapi.api.IQOptionAPI>`.
        """
        super(DBHLC, self).__init__(api, active)
        self.name = "DBHLC"

    def put(self):
        """Method to check put pattern."""
        logger = logging.getLogger("__main__")
        candles = self.candles

        if hasattr(candles, 'first_candle') and hasattr(candles, 'second_candle'):
            up, lw = self.bolinger_bands(candles=candles)

            if candles.first_candle.candle_high >= up[26]:
                if candles.first_candle.candle_high == candles.second_candle.candle_high:
                    if candles.second_candle.candle_close < candles.first_candle.candle_low:
                        logger.info("Upper Band:'%f', First candle high: '%f'.", up[26], candles.first_candle.candle_high)
                        logger.info("First candle high:'%f', Second candle high: '%f'.", candles.first_candle.candle_high, candles.second_candle.candle_high)
                        logger.info("Second candle close:'%f', First candle low: '%f'.", candles.second_candle.candle_close, candles.first_candle.candle_low)
                        return True
