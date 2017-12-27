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
            up, lw = self.bolinger_bands(candles=candles)

            if candles.first_candle.candle_high >= int(round(up[25])):
                if candles.first_candle.candle_close >= candles.second_candle.candle_high:
                    if candles.second_candle.candle_close <= candles.first_candle.candle_low:
                        return True

    def call(self):
        """Method to check call pattern."""
        candles = self.candles

        if hasattr(candles, 'first_candle') and hasattr(candles, 'second_candle'):
            up, lw = self.bolinger_bands(candles=candles)
            if candles.first_candle.candle_low <= int(round(lw[25])):
                if candles.first_candle.candle_close <= candles.second_candle.candle_low:
                    if candles.second_candle.candle_close >= candles.first_candle.candle_high:
                        return True
