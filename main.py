import asyncio
import logging
from src.core.telegram_extractor import TelethonExtractorProcess
from src.handler.messages_handler import MessageHandler


async def main():
    logging.info("Starting TelethonExtractorProcess and MessageHandler...")

    extractor = TelethonExtractorProcess()
    handler = MessageHandler()

    # Using create_task for concurrent execution
    extractor_task = asyncio.create_task(extractor.clients_start())
    handler_task = asyncio.create_task(handler.read_from_redis())

    await asyncio.gather(extractor_task, handler_task)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting main event loop...")

    asyncio.run(main())

    logging.info("Main event loop finished.")

