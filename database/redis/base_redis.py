from redis import Redis
from typing import Any


class BaseRedisDao:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        self.connection = None

    def get_connection(self) -> Any:
        if self.connection is None or self.connection.ping() is False:
            self.connection = Redis(host=self.host,
                                    port=self.port,

                                    )
        return self.connection
