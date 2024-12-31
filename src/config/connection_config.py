import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()


class RedisConfig:
    REDIS_SERVER_IP = os.getenv("REDIS_SERVER_IP")
    REDIS_SERVER_PORT = os.getenv("REDIS_SERVER_PORT", 6385)
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    REDIS_USER = os.getenv("REDIS_USER")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

    REDIS_DUPLICATION_SERVER_IP = os.getenv("REDIS_DUPLICATION_SERVER_IP")
    REDIS_DUPLICATION_SERVER_PORT = os.getenv("REDIS_DUPLICATION_SERVER_PORT", 6379)
    REDIS_DUPLICATION_DB = int(os.getenv("REDIS_DUPLICATION_DB", 0))
    REDIS_DUPLICATION_USER = os.getenv("REDIS_DUPLICATION_USER")
    REDIS_DUPLICATION_PASSWORD = os.getenv("REDIS_DUPLICATION_PASSWORD", None)


class LoggingConfig:
    MODE = os.getenv("MODE", "DEBUG")
    LOGSTASH_HOST = os.getenv("LOGSTASH_HOST")
    LOGSTASH_PORT = int(os.getenv("LOGSTASH_PORT"))


class MySQLConnection:
    # Database connection details from environment variables
    __DB_HOST = os.getenv('DB_HOST', 'localhost')
    __DB_USERNAME = os.getenv('DB_USERNAME', 'root')
    __DB_PASSWORD = os.getenv('DB_PASSWORD', 'admin')
    __DATABASE_NAME = os.getenv('DATABASE_NAME', 'dibaache')

    # Create the database URL
    __DATABASE_URL = f"mysql+pymysql://{__DB_USERNAME}:{__DB_PASSWORD}@{__DB_HOST}/{__DATABASE_NAME}"

    # Create the engine
    __engine = create_engine(__DATABASE_URL)

    # Create a configured session class
    __SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=__engine)

    # Create a base class for the models
    Base = declarative_base()

    @classmethod
    def get_session(cls):
        """Get a new session for interacting with the database."""
        return cls.__SessionLocal()

    @classmethod
    def create_all_tables(cls):
        """Create all tables in the database."""
        cls.Base.metadata.create_all(cls.__engine)


class KafkaConfig:
    KAFKA_BROKER = os.getenv("KAFKA_BROKER")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
    KAFKA_ACK = os.getenv("KAFKA_ACK", 'all')
    KAFKA_LINGER_MS = int(os.getenv("KAFKA_LINGER_MS", 5))
    KAFKA_BATCH_NO = int(os.getenv("KAFKA_BATCH_NO", 50))
    KAFKA_BATCH_TIMEOUT = int(os.getenv("KAFKA_BATCH_TIMEOUT", 10))
