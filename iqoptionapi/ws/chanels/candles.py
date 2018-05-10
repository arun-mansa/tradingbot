"""Module for IQ option candles websocket chanel."""

from iqoptionapi.ws.chanels.base import Base


class GetCandles(Base):
    """Class for IQ option candles websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "sendMessage"

    def __call__(self, active_id, duration, period):
        """Method to send message to candles websocket chanel.

        :param active_id: The active identifier.
        :param duration: The candle duration.
        """
        server_timestamp = self.api.timesync.server_timestamp - (16 * 3600 * 0)

        data = {
            "name":"get-candles",
            "version":"2.0",
            "body": {
                "active_id": active_id,
                "size": duration,
                "from": server_timestamp - (duration * period),
                "to": server_timestamp,
                "chunk_size": period,
            }
        }

        self.send_websocket_request(self.name, data, str(active_id))
