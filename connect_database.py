from sqlalchemy import create_engine

from dotenv import load_dotenv

load_dotenv()
import os

url_database = os.environ.get("URL_DATABASE")

engine = create_engine(url_database)
