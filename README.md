# TelegramScraper
"A scalable Telegram message and media scraper for monitoring and collecting channel data in real-time."
# Telegram Scraping with Redis Integration

This project allows you to scrape messages from Telegram channels using the `Telethon` library, download any media included in those messages (photos, videos), and store the data in Redis for real-time processing. Additionally, it integrates with MySQL for persistent data storage.

## Table of Contents
- [Project Overview](#project-overview)
- [Installation Instructions](#installation-instructions)
- [Configuration](#configuration)
  - [Redis Configuration](#redis-configuration)
  - [MySQL Configuration](#mysql-configuration)
- [Telegram Clients](#telegram-clients)
- [Media Downloading](#media-downloading)
- [Running the Application](#running-the-application)
- [Error Handling and Logging](#error-handling-and-logging)
- [Contributing](#contributing)


## Project Overview

This project leverages multiple Telegram clients to listen for new messages, download media, and store the data in Redis for real-time processing. It also interacts with a MySQL database to store metadata or track processing information.

### Key Features:
- Multiple Telegram clients for scalable message scraping
- Real-time message and media downloading
- Redis queues for efficient message handling
- MySQL database integration for persistent storage

---

## Installation Instructions

### Prerequisites
Make sure you have the following installed:
- Python 3.7+
- Redis server
- MySQL server

### Install Dependencies

Clone this repository:

```bash
git clone https://github.com/yourusername/telegram-scraping.git
cd telegram-scraping
```
### Install the required dependencies:
```bash
pip install -r requirements.txt
```
## Configuration

### Redis Configuration

The `CollectionRedisDao` class interacts with Redis to store and retrieve messages. Make sure your `REDIS_SERVER_IP` and `REDIS_SERVER_PORT` are correctly set in your environment variables or configuration file.

The following methods are available in the `CollectionRedisDao` class:

- **`user_exists(channel_id: str) -> bool`**: Checks if a user exists in the Redis database for a given `channel_id`.
- **`set_user_retry_time(channel_id: str, wait_time: int) -> None`**: Sets the retry time for a user in Redis.
- **`get_user_retry_time(channel_id: str) -> float`**: Retrieves the retry time for a given user.
- **`push_message_to_queue(channel_id: str, message_data: dict)`**: Pushes a message into the Redis queue for the specified `channel_id`.
- **`get_messages_from_queue(channel_id: str) -> Any`**: Retrieves a message from the Redis queue for the specified `channel_id`.

### MySQL Configuration

The `BaseDao` class interacts with MySQL. Ensure that your MySQL credentials are correctly set up for the `MySQLConnection` class in the configuration file.

The following method is used to execute statements in the MySQL database:

- **`execute_statement(statement)`**: Executes an SQL statement against the database and returns the result.

### Telegram Clients

#### Initialization

The `TelethonExtractorProcess` class is responsible for managing multiple Telegram clients. Each client is configured with an API ID, API hash, and phone number. The clients are initialized and connected to Telegram's servers.

To initialize the clients, the `initialize_clients()` method is used.

#### Telegram Message Listening

Once the clients are connected, the method `_start_listening(client)` listens for new messages on the Telegram channels.

### Media Downloading

#### TelegramAdapter

The `TelegramAdapter` class handles downloading media from Telegram messages. It supports downloading photos, videos, and other media types.

##### Methods:

- **`download_media(client, message, channel_username)`**: Downloads media (photos or videos) from a message and stores it in the appropriate directory based on the channel's username.

##### Example usage:

```python
media_info = await TelegramAdapter.download_media(client, message, channel_username)
```
### Running the Application

After setting up your configuration, run the application with:

```bash
python main.py
```
This will start the Telegram clients, listen for new messages, and handle media  downloading and message processing in real-time. 

### Error Handling and Logging

The project uses Python's built-in logging module for error and event logging. You can configure the logging level in `main.py` by modifying the `logging.basicConfig()` call.

Example logging configuration:

```python
logging.basicConfig(level=logging.INFO)
```
### Contributing

We welcome contributions to this project! To contribute:

1. Fork the repository
2. Make your changes in a new branch
3. Submit a pull request
4. Be sure to write tests for any new features or bug fixes.

