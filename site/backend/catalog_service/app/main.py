import uvicorn, os
from modules.api.app import app
from modules.utils.logger import logger


def main() -> None:
    # Когда вы запускаете FastAPI с host='127.0.0.1' внутри Docker контейнера, только процессы внутри контейнера могут подключаться к приложению, так как 127.0.0.1 доступен только в рамках контейнера. Однако, если вы используете host='0.0.0.0', контейнер слушает на всех интерфейсах, включая внешний интерфейс контейнера, и ваше приложение становится доступным и на внешнем IP-адресе, что позволяет вам подключаться к нему с хоста или других контейнеров
    # Порт должен быть именно число, не строкой
    uvicorn.run(app=app, host=os.getenv('APP_HOST'), port=int(os.getenv('APP_PORT')))  # host='0.0.0.0' внутри контейнера
    # uvicorn.run(app=app, host='127.0.0.1', port=8001)  # host='0.0.0.0' вне контейнера

if __name__ == "__main__":
    main()
    
# from modules.db.db_manager import db
# db.create_tables()
# db.test_fill_in()

# logger.info(f'xxx')