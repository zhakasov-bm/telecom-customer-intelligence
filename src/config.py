import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine

BASE_DIR = Path(__file__).resolve().parents[1]

load_dotenv(BASE_DIR / ".env")

RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "telco_customer_churn.csv"

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    host=os.environ["POSTGRES_HOST"],
    port=int(os.environ["POSTGRES_PORT"]),
    database=os.environ["POSTGRES_DB"],
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)
