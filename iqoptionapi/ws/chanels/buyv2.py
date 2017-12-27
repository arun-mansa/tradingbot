"""Module for IQ Option buyV2 websocket chanel."""

from iqoptionapi.ws.chanels.base import Base
import numpy as np

class Buyv2(Base):
    """Class for IQ option buy websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "buyV2"

    def __call__(self, price, active, option, direction):
        """Method to send message to buyv2 websocket chanel.

        :param price: The buying price.
        :param active: The buying active.
        :param option: The buying option.
        :param direction: The buying direction.
        """
        data = {"price": price,
                "act": active,
                "exp": np.int64(self.api.timesync.expiration_timestamp),
                "type": option,
                "direction": direction,
                "user_balance_id": self.api.profile.balance_id,
                "time": self.api.timesync.server_timestamp,
                "skey": self.api.profile.skey
               }

        self.send_websocket_request(self.name, data)
