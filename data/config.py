import os
from dotenv import load_dotenv

load_dotenv()
token = str(os.getenv("token"))

admin_id = [

]

ip = os.getenv('ip')

PGUSER = str(os.getenv('PGUSER'))
PGPASSWORD = str(os.getenv('PGPASSWORD'))
DATABASE = str(os.getenv('DATABASE'))

POSTGRES_URL = f'postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}'