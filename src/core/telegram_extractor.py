import logging
import random
import asyncio
from telethon import events
from typing import List, Any, Dict, Optional
from src.config.static_config import StaticConfig
from src.data.dal.collection_dal import CollectionDal
from src.data.dao.redis.collection_redis import CollectionRedisDao
from src.enums.telegram_clients import Client
from src.media_manager.telegram_adaptor import TelegramAdapter


class TelethonExtractorProcess:
    def __init__(self):
        collection_dal = CollectionDal()

        clients: List[Dict[str, Any]] = StaticConfig.TELEGRAM_CLIENTS
        self.channel_usernames_by_phone_number = collection_dal.get_client_channel_map()
        self.client_tel = Client(clients)
        self.telegram_adapter = TelegramAdapter()
        self.collection_redis_dao = CollectionRedisDao()
        self.min_sleep_time = StaticConfig.MIN_TIME_SLEEP_HANDLER_SCRAPY
        self.max_sleep_time = StaticConfig.MAX_TIME_SLEEP_HANDLER_SCRAPY

    async def _start_listening(self, client) -> None:
        await client.start()
        client_phone = client.phone_number

        channel_usernames: List[str] = await self._get_channel_usernames(client)
        logging.info(f"Listening for new messages on channels: {channel_usernames} with phone {client_phone}")

        @client.on(events.NewMessage(chats=channel_usernames))
        async def handler(event: Any) -> None:

            channel_id = event.message.peer_id.channel_id
            media_info: Dict[str, Optional[str]] = {"file_path": None, "media_type": None}
            channel_entity = await client.get_entity(channel_id)
            channel_username = channel_entity.username if channel_entity.username else "unknown"

            if event.message.media:
                print("Media found, downloading...")
                media_info = await self.telegram_adapter.download_media(client, event.message, channel_username)
                print(f"Media downloaded to: {media_info}")

            else:
                print("No media found.")
            media_path: Optional[str] = media_info.get('media_path', None)
            media_type: Optional[str] = media_info.get('media_type', None)
            message_data = {
                "message_id": event.id,
                "text": event.message.message,
                "media_path": media_path,
                "media_type": media_type,
                "date": event.message.date.isoformat(),
                "from_id": event.message.from_id,
                "phone_number": client_phone,
                "channel_id": channel_id,
                "channel_username": channel_username,
            }
            await self.send(message_data)
            logging.info(f"Message sent to Redis: {message_data}")
            await asyncio.sleep(random.uniform(self.min_sleep_time, self.max_sleep_time))

        logging.info(f"Starting Telegram client for phone {client_phone} to listen for messages...")
        await client.run_until_disconnected()

    async def _get_channel_usernames(self, client) -> List[str]:
        # Filter channels based on the client's phone number
        client_phone = client.phone_number
        if client_phone in self.channel_usernames_by_phone_number:
            return self.channel_usernames_by_phone_number[client_phone]
        else:
            return []

    async def clients_start(self) -> None:
        logging.info("Initializing Telegram clients...")
        await self.client_tel.initialize_clients()  # Asynchronous call to initialize clients
        logging.info("Starting all Telegram clients...")
        await asyncio.gather(*(self._start_listening(client) for client in self.client_tel.get_clients()))
        logging.info("All Telegram clients started successfully.")

    async def send(self, event_data: Dict[str,Any]) -> None:
        logging.info("Sending message to queue...")
        print("Sending message to queue:", event_data)
        redis_dao = self.collection_redis_dao
        redis_dao.push_message_to_queue(event_data['channel_username'], event_data)
