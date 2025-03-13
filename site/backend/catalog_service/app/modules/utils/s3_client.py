import time, random, datetime
from pathlib import Path
from contextlib import asynccontextmanager
from aiobotocore.session import get_session
from botocore.exceptions import ClientError
import asyncio, aiofiles, json, requests, os


class S3Client:
    def __init__(self, access_key: str, secret_key: str, endpoint_url: str, region_name: str):
        self.config = {
            'aws_access_key_id': access_key,
            'aws_secret_access_key': secret_key,
            'endpoint_url': endpoint_url,
            'region_name': region_name  # Регион (не важен для MinIO)
        }
        self.session = get_session()
        
    async def upload_file(self, file_path: str, bucket_name: str) -> str:
        await self._try_create_bucket(bucket_name)
        
        file_name = file_path.split('/')[-1]
        file_extension = os.path.splitext(file_name)[1]
        uid = f"{time.time()}.{random.randint(0, 9999)}{file_extension}"

        async with self._get_client() as client:
            with open(file_path, "rb") as f:
                await client.put_object(Bucket=bucket_name, Key=uid, Body=f)
                
        return uid
            
    async def create_presigned_url(self, bucket_name: str, object_name: str, expiration: int) -> str:
        async with self._get_client() as client:
            return await client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': object_name},
                ExpiresIn=expiration
            )
            
    @asynccontextmanager
    async def _get_client(self):
        async with self.session.create_client('s3', **self.config) as client:
            yield client
    
    async def _try_create_bucket(self, bucket_name: str):
        async with self._get_client() as client:
            try:
                await client.head_bucket(Bucket=bucket_name)
              
            except ClientError as e:
                await client.create_bucket(Bucket=bucket_name)
            
            
s3_client = S3Client(
    access_key=os.getenv('MINIO_ACCESS_KEY'), 
    secret_key=os.getenv('MINIO_SECRET_KEY'), 
    endpoint_url=os.getenv('MINIO_ENDPOINT'),
    region_name=os.getenv('MINIO_REGION_NAME')
)