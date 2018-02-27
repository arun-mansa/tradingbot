"""Module for IQ Option API SPINTOP pattern."""

from base import Base


class SPINTOP(Base):
    """Class for SPINTOP pattern."""

    def __init__(self, api, active):
        """
        :param api: The instance of
            :class:`IQOptionAPI <iqoptionapi.api.IQOptionAPI>`.
        """
        super(SPINTOP, self).__init__(api, active)
        self.name = "SPINTOP"

    def call(self):
        """Method to check call pattern."""
        if self.candles:
            return True

    def put(self):
        """Method to check put pattern."""
        if self.candles:
            return True
