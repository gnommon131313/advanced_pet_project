import sqlalchemy, os
from sqlalchemy.orm import Session

from modules.db import models


class DBManager:
    
    def __init__(self) -> None:
        self.engine = sqlalchemy.create_engine(
            url=f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@user_db:5432/{os.getenv("POSTGRES_DB")}', 
            echo=True
        )

    def create_session(self) -> Session:
        return Session(self.engine)
    
    def create_tables(self) -> None:
        models.Base.metadata.create_all(bind=self.engine)
        
    def test_fill_in(self):
        with self.create_session() as session:
            users = [
                models.User(chat_id="111", phone = "111", name='name 1', last_name='last_name 1'),
                models.User(chat_id="222", phone = "222", name='name 2', last_name='last_name 2'),
                models.User(chat_id="333", phone = "333", name='name 3', last_name='last_name 3'),
                models.User(chat_id="444", phone = "444", name='name 4', last_name='last_name 4'),
            ]
            
            for x in users:
                session.add(x)
            
            session.commit()
    
    
db = DBManager()