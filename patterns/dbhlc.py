"""Module for IQ Option API DBHLC pattern."""

from base import Base


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
        candles = self.candles

        if hasattr(candles, 'first_candle') and hasattr(candles, 'second_candle'):
            rsi = self.rsi(candles, 14)
            if candles.first_candle.candle_high == candles.second_candle.candle_high:
                if rsi[27] >= 70.0 and candles.second_candle.candle_close <= candles.first_candle.candle_open:
                    return True