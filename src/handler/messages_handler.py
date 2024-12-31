import json
import logging
import random
import asyncio
from typing import List, Any, Dict
from kafka import KafkaProducer
from src.config.connection_config import KafkaConfig
from src.config.static_config import StaticConfig
from src.data.dal.collection_dal import CollectionDal
from src.data.dao.redis.collection_redis import CollectionRedisDao


class MessageHandler:
    def __init__(self) -> None:
        self.redis_dao = CollectionRedisDao()
        self.collection_dal = CollectionDal()
        self.min_sleep_time = StaticConfig.MIN_TIME_SLEEP_MESSAGE_HANDLER
        self.max_sleep_time = StaticConfig.MAX_TIME_SLEEP_MESSAGE_HANDLER
        self.producer = KafkaProducer(
            bootstrap_servers=KafkaConfig.KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.kafka_topic = KafkaConfig.KAFKA_TOPIC

    async def read_from_redis(self) -> None:

        channel_usernames: List[str] = self.collection_dal.get_channel_username()
        logging.info(f"MessageHandler started. Listening to channel_username in Redis: {channel_usernames}")

        while True:
            for channel_username in channel_usernames:
                message_data: Dict[str, Any] = self.redis_dao.get_messages_from_queue(channel_username)
                if message_data:
                    await self.process_message(message_data)
            await asyncio.sleep(random.uniform(self.min_sleep_time, self.max_sleep_time))

    async def process_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        logging.info(f"Processing message handler: {message_data['text']}")
        print(f"Processing message handler: {message_data}")

        await self.send_to_kafka(message_data)

        return message_data

    async def send_to_kafka(self, message_data: Dict[str, Any]) -> None:
        try:
            await asyncio.to_thread(self.producer.send, self.kafka_topic, value=message_data)
            logging.info(f"Message sent to Kafka: {message_data}")
        except Exception as e:
            logging.error(f"Failed to send message to Kafka: {e}")
