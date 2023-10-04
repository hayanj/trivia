import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.environ.get("DB_NAME")
DB_USER=os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_TESTNAME = os.environ.get("DB_TESTNAME")
DB_HOST = os.environ.get("DB_HOST")