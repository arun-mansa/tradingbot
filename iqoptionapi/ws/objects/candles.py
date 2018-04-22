"""Module for IQ Option Candles websocket object."""

from iqoptionapi.ws.objects.base import Base


class Candle(object):
    """Class for IQ Option candle."""

    def __init__(self, candle_data):
        """
        :param candle_data: The list of candles data.
        """
        self.__candle_data = candle_data

    @property
    def candle_time(self):
        """Property to get candle time.

        :returns: The candle time.
        """
        return self.__candle_data['from']

    @property
    def candle_open(self):
        """Property to get candle open value.

        :returns: The candle open value.
        """
        return self.__candle_data['open'] * 1000000

    @property
    def candle_close(self):
        """Property to get candle close value.

        :returns: The candle close value.
        """
        return self.__candle_data['close'] * 1000000

    @property
    def candle_high(self):
        """Property to get candle high value.

        :returns: The candle high value.
        """
        return self.__candle_data['max'] * 1000000

    @property
    def candle_low(self):
        """Property to get candle low value.

        :returns: The candle low value.
        """
        return self.__candle_data['min'] * 1000000

    @property
    def candle_type(self):
        """Property to get candle type value.

        :returns: The candle type value.
        """
        if self.candle_open < self.candle_close:
            return "green"
        elif self.candle_open > self.candle_close:
            return "red"

    @property
    def candle_height(self):
        """Property to get candle height value.

        :returns: The candle type value.
        """
        if self.candle_open < self.candle_close:
            return self.candle_close - self.candle_open
        elif self.candle_open > self.candle_close:
            return self.candle_open - self.candle_close
        else:
            return 0

    @property
    def upper_shadow(self):
        """Property to get candle height value.

        :returns: The candle type value.
        """
        if self.candle_type == "green":
            return self.candle_high - self.candle_close
        elif self.candle_open > self.candle_close:
            return self.candle_high - self.candle_open

    @property
    def lower_shadow(self):
        """Property to get candle height value.

        :returns: The candle type value.
        """
        if self.candle_type == "green":
            return self.candle_high - self.candle_open
        elif self.candle_open > self.candle_close:
            return self.candle_high - self.candle_close

    @property
    def is_spinning_top(self):
        """Property to get candle close value.

        :returns: The candle close value.
        """

        if self.candle_height > 1 and self.upper_shadow >= (5 * self.candle_height):
            return True
        elif self.candle_height > 1 and self.upper_shadow < (5 * self.candle_height):
            return False



class Candles(Base):
    """Class for IQ Option Candles websocket object."""

    def __init__(self):
        super(Candles, self).__init__()
        self.__name = "candles"
        self.__candles_data = None

    @property
    def candles_data(self):
        """Property to get candles data.

        :returns: The list of candles data.
        """
        return self.__candles_data

    @candles_data.setter
    def candles_data(self, candles_data):
        """Method to set candles data."""
        self.__candles_data = candles_data

    @property
    def first_candle(self):
        """Method to get first candle.

        :returns: The instance of :class:`Candle
            <iqoptionapi.ws.objects.candles.Candle>`.
        """
        return Candle(self.candles_data[-3])

    @property
    def second_candle(self):
        """Method to get second candle.

        :returns: The instance of :class:`Candle
            <iqoptionapi.ws.objects.candles.Candle>`.
        """
        return Candle(self.candles_data[-2])

    @property
    def current_candle(self):
        """Method to get current candle.

        :returns: The instance of :class:`Candle
            <iqoptionapi.ws.objects.candles.Candle>`.
        """
        return Candle(self.candles_data[-1])

    @property
    def candles_array(self):
        """Method to all candles_data as array of Candle class.

        :returns: The arrya of :class:`Candle
            <iqoptionapi.ws.objects.candles.Candle>`.
        """
        return [Candle(data) for data in self.candles_data]
