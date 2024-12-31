import time
from typing import Any, Dict
import json
from src.config.connection_config import RedisConfig
from src.data.dao.redis.base_redis_dao import BaseRedisDao


class CollectionRedisDao(BaseRedisDao):
    def __init__(self):
        super().__init__(host=RedisConfig.REDIS_SERVER_IP,
                         port=RedisConfig.REDIS_SERVER_PORT,
                         # user=RedisConfig.REDIS_USER,
                         # password=RedisConfig.REDIS_PASSWORD,
                         # db=RedisConfig.REDIS_DB
                         )

    def user_exists(self, channel_id: str) -> bool:
        return bool(self.get_connection().exists(channel_id))

    def set_user_retry_time(self, channel_id: str, wait_time: int) -> None:
        expiration_time = time.time() + wait_time
        self.get_connection().setex(channel_id, wait_time, expiration_time)

    def get_user_retry_time(self, channel_id: str) -> float:
        return float(self.get_connection().get(channel_id) or 0)

    def push_message_to_queue(self, channel_id: str, message_data: dict):
        """
        Push a message to the Redis queue for the specified channel ID.

        Args:
            channel_id (str): The ID of the channel (used as the Redis key).
            message_data (dict): The message data to be pushed to the queue.
        """
        # Directly use the channel_id as the Redis key
        queue_name = channel_id  # Use the channel_id directly
        # Serialize the message_data dictionary to a JSON string
        message_json = json.dumps(message_data)
        self.get_connection().rpush(queue_name, message_json)  # Push message to the channel ID key

    def get_messages_from_queue(self, channel_id: str) -> Any:
        """
        Get a message from the Redis list for the specified channel ID.

        Args:
            channel_id (str): The ID of the channel (used as the Redis key).

        Returns:
            Any: The message data as a dictionary, or None if the queue is empty.
        """
        # Use the channel_id directly as the Redis key
        queue_name = channel_id  # Use the channel_id directly
        message_json = self.get_connection().lpop(queue_name)  # Pop message from the channel ID key
        if message_json:
            return json.loads(message_json)  # Convert the JSON string back to a dictionary
        return None
