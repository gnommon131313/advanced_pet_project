import sqlalchemy, os
from sqlalchemy.orm import Session

from modules.db import models


class DBManager:
    
    def __init__(self) -> None:
        self.engine = sqlalchemy.create_engine(
            # Мысли на счет того как подлючаться в одних контейнерах к другим
            # Тут чтобы подключиться к БД нужен её адрес и порт (...@адрес:порт/...)
            # Адрес можно использовать по разному, а порт задаветься явно вручную в самом docker compose
            # `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' имя контейнера` - узнать адрес контейнера
            
            # 1) Правильный способ - по имени контейнера (порт указвать внутрений в контейнере, а не как какой он замаплен на хосте)
            url=f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@catalog_db:5432/{os.getenv("POSTGRES_DB")}', 
            
            # 2) Не правильный но рабочий способ - по ip адресу контейнера
            # Адреса выдаються докером динамически при поднятии контейнера и не являються константой для конкретного контейнера
            # url=f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@172.18.0.2:5432/{os.getenv("POSTGRES_DB")}', 
            
            # 3) Вообще не правильный способ - тут 127.0.0.1 (localhost) доступен только внутри самого этого контейнера, а нам нужен его адрес другого контейнера к которому мы хотим подключиться
            # url=f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@127.0.0.1:5432/{os.getenv("POSTGRES_DB")}', 
            
            # 4) Вообще не правильный способ - некоректный адрес
            # url=f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@6.6.6.6:5432/{os.getenv("POSTGRES_DB")}', 
            echo=True
        )

    def create_session(self) -> Session:
        return Session(self.engine)
    
    def create_tables(self) -> None:
        models.Base.metadata.create_all(bind=self.engine)
        
    def test_fill_in(self):
        with self.create_session() as session:
            products = [
                models.Product(name="thing 1", description = "super", price=11.0, image=f"1741690101.5923717.407.png"),
                models.Product(name="thing 2", description = "super", price=22.0, image=f"1741690102.0949545.1159.png"),
                models.Product(name="thing 3", description = "super", price=33.0, image=f"1741690102.5534654.5666.png"),
                models.Product(name="thing 4", description = "super", price=44.0, image=f"1741690102.9725237.7927.png"),
                models.Product(name="thing 5", description = "super", price=55.0, image=f"1741690103.4805727.9818.png"),
                models.Product(name="thing 6", description = "super", price=66.0, image=f"1741690103.975115.416.png"),
                models.Product(name="thing 7", description = "super", price=77.0, image=f"1741690104.4376163.6271.png"),
                models.Product(name="thing 8", description = "super", price=88.0, image=f"1741690104.9205747.4292.png"),
                models.Product(name="thing 9", description = "super", price=99.0, image=f"1741690105.370212.7346.png"),
                models.Product(name="thing 10", description = "super", price=100.0, image=f"1741690105.8208623.4085.png"),
                models.Product(name="thing 11", description = "super", price=111.0, image=f"1741690106.271367.3998.png"),
                models.Product(name="thing 12", description = "super", price=122.0, image=f"1741690106.7250893.4395.png"),
                models.Product(name="thing 13", description = "super", price=133.0, image=f"1741690107.1767387.6334.png"),
            ]
            
            for x in products:
                session.add(x)
            
            session.commit()
    
    
db = DBManager()