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
            
            # 1) Правильный способ - по имени контейнера 
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
                models.Product(name="thing 1", description = "super", price=11.0, image=f"Egg.png"),
                models.Product(name="thing 2", description = "super", price=22.0, image=f"EggRaw.png"),
                models.Product(name="thing 3", description = "super", price=33.0, image=f"EggsFried.png"),
                models.Product(name="thing 4", description = "super", price=44.0, image=f"Fish.png"),
                models.Product(name="thing 5", description = "super", price=55.0, image=f"FishCut.png"),
                models.Product(name="thing 6", description = "super", price=66.0, image=f"FishFried.png"),
                models.Product(name="thing 7", description = "super", price=77.0, image=f"FishSkeleton.png"),
                models.Product(name="thing 8", description = "super", price=88.0, image=f"FriedMeat.png"),
                models.Product(name="thing 9", description = "super", price=99.0, image=f"GarbageBag.png"),
                models.Product(name="thing 10", description = "super", price=100.0, image=f"Meat.png"),
                models.Product(name="thing 11", description = "super", price=111.0, image=f"MeatCut.png"),
                models.Product(name="thing 12", description = "super", price=122.0, image=f"PiecesOfMeat.png"),
                models.Product(name="thing 13", description = "super", price=133.0, image=f"XX.png"),
                models.Product(name="thing 14", description = "super", price=144.0, image=f"XX.png"),
                models.Product(name="thing 15", description = "super", price=155.0, image=f"XX.png"),
                models.Product(name="thing 16", description = "super", price=166.0, image=f"XX.png"),
            ]
            
            for x in products:
                session.add(x)
            
            session.commit()
    
    
db = DBManager()