import logging
import os
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from typing import Any, Dict, Optional
from src.config.static_config import StaticConfig


class TelegramAdapter:

    @staticmethod
    async def download_media(client, message: Any, channel_username: str) -> Dict[str, Optional[str]]:

        media_folder = StaticConfig.MEDIA_FOLDER
        os.makedirs(media_folder, exist_ok=True)

        # channel_id = message.peer_id.channel_id

        channel_folder = os.path.join(media_folder, str(channel_username))
        os.makedirs(channel_folder, exist_ok=True)

        photo_folder = os.path.join(channel_folder, "photos")
        video_folder = os.path.join(channel_folder, "videos")
        os.makedirs(photo_folder, exist_ok=True)
        os.makedirs(video_folder, exist_ok=True)

        media_info: Dict[str, Optional[str]] = {"media_path": None, "media_type": None}
        if message.media:
            if isinstance(message.media, MessageMediaPhoto):
                logging.info(f"Downloading photo from channel '{channel_username}'...")
                media_info["media_path"] = await client.download_media(message, file=photo_folder)
                media_info["media_type"] = 'photo'
                logging.info(f"Photo downloaded successfully to: {media_info['media_path']}")
            elif isinstance(message.media, MessageMediaDocument):
                logging.info(f"Downloading video from channel '{channel_username}'...")
                media_info["media_path"] = await client.download_media(message, file=video_folder)
                media_info["media_type"] = 'video'
                logging.info(f"Video downloaded successfully to: {media_info['media_path']}")
        else:
            logging.info(f"No media found in the message from channel '{channel_username}'.")
        return media_info
