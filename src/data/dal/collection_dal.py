from src.config.connection_config import MySQLConnection
from src.data.dao.mysql.collection_dao import CollectionDao


class CollectionDal:
    def __init__(self):
        pass

    @staticmethod
    def get_client_channel_map():
        session = MySQLConnection.get_session()
        try:
            channels = session.query(
                CollectionDao.phone_number,
                CollectionDao.username
            ).filter(CollectionDao.deleted == False).all()

            client_channel_map = {}
            for channel in channels:
                phone_number = channel.phone_number
                channel_usernames = channel.username

                if phone_number not in client_channel_map:
                    client_channel_map[phone_number] = []

                client_channel_map[phone_number].append(channel_usernames)

            return client_channel_map
        except Exception as e:
            print(f"An error occurred while fetching channel map data: {e}")
            return {}
        finally:
            session.close()

    def get_channel_username(self):
        session = MySQLConnection.get_session()
        try:
            channels = session.query(CollectionDao.username).filter(CollectionDao.deleted == False).all()
            return [channel[0] for channel in channels]
        except Exception as e:
            print(f"An error occurred while fetching channel names: {e}")
        finally:
            session.close()

    def get_channel_id(self):
        session = MySQLConnection.get_session()
        try:
            channel_ids = session.query(CollectionDao.profile_id).filter(CollectionDao.deleted == False).all()
            return [channel_id[0] for channel_id in channel_ids]
        except Exception as e:
            print(f"An error occurred while fetching channel ids: {e}")
        finally:
            session.close()


# if __name__ == "__main__":
#     dal = CollectionDal()
#
#     c = dal.get_client_channel_map()
#     print("Client Channel Map:", c)

