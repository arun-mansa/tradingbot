"""Module for IQ Option API DBLHC pattern."""

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
        candles = self.candles

        if hasattr(candles, 'first_candle') and hasattr(candles, 'second_candle'):
            up, lw = self.bolinger_bands(candles=candles)

            if candles.first_candle.candle_low <= int(round(lw[26])):
                if candles.first_candle.candle_low == candles.second_candle.candle_low:
                    if candles.second_candle.candle_close > candles.first_candle.candle_low:
                        return True

