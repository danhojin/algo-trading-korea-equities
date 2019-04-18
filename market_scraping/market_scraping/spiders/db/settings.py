import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

PG_USERNAME = os.getenv('PG_USERNAME')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_HOST = os.getenv('PG_HOST')
PG_DATABASE = os.getenv('PG_DATABASE')
