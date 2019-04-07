import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
KW_CONTROL_CLSID = os.getenv("KW_CONTROL_CLSID")
KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER")