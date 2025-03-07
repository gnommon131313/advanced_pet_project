import uvicorn, os
from modules.fast_api.app import app
from modules.utils.logger import logger


# def main() -> None:
#     uvicorn.run(app=app, host=os.getenv('APP_HOST'), port=int(os.getenv('APP_PORT')))

# if __name__ == "__main__":
#     main()
    
from modules.db.db_manager import db
db.create_tables()
db.test_fill_in()