import datetime
from typing import Optional
from src.data.dao.mysql.base_dao import BaseDao
from src.config.connection_config import MySQLConnection
from sqlalchemy import Column, Integer, String, DateTime, Boolean


class CollectionDao(BaseDao):
    __tablename__ = 'telegram'

    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    profile_id = Column(String(255), nullable=True)
    username = Column(String(50), nullable=False)
    fullname = Column(String(200), nullable=False)
    last_visit_time = Column(DateTime, nullable=False)
    domain = Column(String(255), nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)
    insert_time = Column(DateTime, nullable=False, default=0)
    picture = Column(String(200), nullable=True)
    phone_number = Column(String(20), nullable=False)

    @staticmethod
    def add_data_to_telegram(url: str, profile_id: str, username: str, fullname: str, domain: str, phone_number: str,
                             picture: Optional[str] = None) -> None:
        session = MySQLConnection.get_session()
        try:
            new_entry = CollectionDao(
                url=url,
                profile_id=profile_id,
                username=username,
                fullname=fullname,
                last_visit_time=datetime.datetime.now(),
                domain=domain,
                deleted=False,
                insert_time=datetime.datetime.now(),
                picture=picture,
                phone_number=phone_number
            )
            session.add(new_entry)
            session.commit()
            print("Data added successfully.")
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
        finally:
            session.close()

# if __name__ == "__main__":
#     CollectionDao.add_data_to_telegram(
#         url="https://t.me/newszariii",
#         profile_id="217267779",
#         username="newszariii",
#         fullname="Zahra News",
#         domain="telegram.com",
#         picture="https://example.com/pic.jpg",
#         phone_number="+981111111111"
#     )
