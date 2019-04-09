import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

KW_CONTROL_CLSID = os.getenv("KW_CONTROL_CLSID")
KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER")
PG_USERNAME = os.getenv('PG_USERNAME')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_HOST = os.getenv('PG_HOST')
PG_DATABASE = os.getenv('PG_DATABASE')