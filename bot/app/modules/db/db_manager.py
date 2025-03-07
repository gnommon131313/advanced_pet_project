import sqlalchemy, os
from sqlalchemy.orm import Session

from modules.db import models


class DBManager:
    
    def __init__(self) -> None:
        self.engine = sqlalchemy.create_engine(os.getenv("DB"), echo=True)

    def create_session(self) -> Session:
        return Session(self.engine)
    
    def create_tables(self) -> None:
        models.Base.metadata.create_all(bind=self.engine)
    
    
db = DBManager()