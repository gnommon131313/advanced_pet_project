# pip install aiobotocore aiohttp aiofiles

import time, random, datetime
from pathlib import Path
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from aiobotocore.session import get_session
from botocore.exceptions import ClientError
import asyncio, aiofiles, json, requests, os


load_dotenv()


class S3Client:
    def __init__(self, access_key: str, secret_key: str, endpoint_url: str, region_name: str):
        self.config = {
            'aws_access_key_id': access_key,
            'aws_secret_access_key': secret_key,
            'endpoint_url': endpoint_url,
            'region_name': region_name  # Регион (не важен для MinIO)
        }
        self.session = get_session()
        
    async def upload_file(self, file_path: str, bucket_name: str):
        # await блокирует поток чтобы завершиться (тут поток это сама функция async)
        await self._try_create_bucket(bucket_name)
        
        # Правильно именно создавать уникальный идентификатор для файла, а потом  загружать его в БД, а не просто использовать имя, т.к. оно может повторяться
        file_name = file_path.split('/')[-1]
        file_extension = os.path.splitext(file_name)[1]
        uid = f"{time.time()}.{random.randint(0, 9999)}{file_extension}"

        async with self._get_client() as client:
            print(f"Загрузка файла {file_path} в бакет {bucket_name}...")
            with open(file_path, "rb") as f:
                await client.put_object(Bucket=bucket_name, Key=uid, Body=f)
            print(f"Файл {file_path} успешно загружен в карзину")
            
    async def del_file(self, file_name: str, bucket_name: str):
        async with self._get_client() as client:
            try:
                print(f"Удаление файла {file_name} из бакета {bucket_name}...")
                await client.delete_object(
                    Bucket=bucket_name,
                    Key=file_name,
                )
                print(f"Файл {file_name} успешно удален.")
                
            except ClientError as e:
                print(f'\nERR: {e} \n')
                
    async def del_bucket(self, bucket_name: str):
        async with self._get_client() as client:
            try:
                # Карзины храняться в томе в контейнере (т.к. тут запуск через docker-compose)
                await client.delete_bucket(Bucket=bucket_name)
                print(f"карзина {bucket_name} успешно удалена")

            except ClientError as e:
                print(f'\nERR: {e} \n')
                
    async def create_presigned_url(self, bucket_name: str, object_name: str, expiration: int):
        async with self._get_client() as client:
            return await client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': object_name},
                ExpiresIn=expiration
            )
            
    # Применить декоратор, чтобы использовать асинхроную функция в менеджере контекстов (чтобы было можно безопасно использовать в 'async with' блоках)
    @asynccontextmanager
    async def _get_client(self):
        async with self.session.create_client('s3', **self.config) as client:
            yield client
    
    async def _try_create_bucket(self, bucket_name: str):
        async with self._get_client() as client:
            try:
                await client.head_bucket(Bucket=bucket_name)
                print(f"Бакет {bucket_name} существует.")
              
            except ClientError as e:
                print(f"Создание бакета {bucket_name}...")

                await client.create_bucket(Bucket=bucket_name)
                # # Настройка публичных прав доступа (политика)
                # # Лучше оставить карзину приватной и для фронта генерировать presigned_url
                # policy = {
                #     "Version": "2012-10-17",
                #     "Statement": [
                #         {
                #             "Effect": "Allow",
                #             "Principal": "*",
                #             "Action": "s3:GetObject",
                #             "Resource": f"arn:aws:s3:::{bucket_name}/*"
                #         }
                #     ]
                # }
                # # Применение политики к карзине (обязательно передавать json, а не просто словарь)
                # await client.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))
            
            
async def main():
    s3_client = S3Client(
        access_key=os.getenv('MINIO_ACCESS_KEY'), 
        secret_key=os.getenv('MINIO_SECRET_KEY'), 
        endpoint_url=os.getenv('MINIO_ENDPOINT'),
        region_name=os.getenv('MINIO_REGION_NAME')
    )
    
    # # Загрузка всех файлов в хранилище
    # path = 'minio/content/images'
    # files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    
    # for f in files:
    #     await s3_client.upload_file(f'{str(path)}/{f}', os.getenv('MINIO_BUCKET_NAME'))
        
    # await s3_client.del_file('12345.12345.png', os.getenv('MINIO_BUCKET_NAME'))
    # await s3_client.del_bucket(os.getenv('MINIO_BUCKET_NAME'))
    
    # Генерация временной ссылки (причем она работает даже если карзина приватная, т.к. это каноничный способ)
    presigned_url = await s3_client.create_presigned_url(
        bucket_name=os.getenv('MINIO_BUCKET_NAME'),
        object_name='1741690101.5923717.407.png', 
        expiration=30  # В секундах
    )  
    print(f'\n {presigned_url} \n')

if __name__ == '__main__':
    asyncio.run(main())