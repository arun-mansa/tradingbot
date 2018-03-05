"""Module for IQ Option API TEST pattern."""

from base import Base
import logging
import csv
import pickle


class TEST(Base):
    """Class for TEST pattern."""

    def __init__(self, api, active):
        """
        :param api: The instance of
            :class:`IQOptionAPI <iqoptionapi.api.IQOptionAPI>`.
        """
        super(TEST, self).__init__(api, active)
        self.name = "TEST"

    def call(self):
        """Method to check call pattern."""
        logger = logging.getLogger("__main__")
        candles = self.candles

        if hasattr(candles, 'first_candle'):
            up, lw, height = self.bolinger_bands(candles=candles)
            rsi7 = self.rsi(candles=candles, period=7)
            rsi14 = self.rsi(candles=candles, period=14)
            rsi28 = self.rsi(candles=candles, period=28)

            loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
            predicted_price = loaded_model.predict([[up[26] - candles.first_candle.candle_close, lw[26] - candles.first_candle.candle_close, candles.first_candle.candle_height - candles.first_candle.candle_height, rsi7[28], rsi14[28], rsi28[28]]])
            logger.info("Predicted price:'%s'", predicted_price[0])
            
            if predicted_price[0] == 1.0:
                return True

    def put(self):
        """Method to check put pattern."""
        candles = self.candles

        if hasattr(candles, 'first_candle'):
            up, lw, height = self.bolinger_bands(candles=candles)
            rsi7 = self.rsi(candles=candles, period=7)
            rsi14 = self.rsi(candles=candles, period=14)
            rsi28 = self.rsi(candles=candles, period=28)

            loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
            predicted_price = loaded_model.predict([[up[26] - candles.first_candle.candle_close, lw[26] - candles.first_candle.candle_close, candles.first_candle.candle_height - candles.first_candle.candle_height, rsi7[28], rsi14[28], rsi28[28]]])

            if predicted_price[0] == -1.0:
                return True
