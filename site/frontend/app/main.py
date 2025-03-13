import uvicorn, os
from api import app


def main() -> None:
    uvicorn.run(app=app, host=os.getenv('APP_HOST'), port=int(os.getenv('APP_PORT')))

if __name__ == "__main__":
    main()