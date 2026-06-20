import os
import logging
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
LOG_DIR = BASE_DIR / 'logs'

# Ensure directories exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, LOG_DIR]:
    os.makedirs(directory, exist_ok=True)

# Database Configuration
# Using SQLite by default for easy local execution without setup.
# To switch to PostgreSQL/MySQL, change the DB_URI below.
# Example PostgreSQL: 'postgresql://username:password@localhost:5432/netflix_db'
# Example MySQL: 'mysql+pymysql://username:password@localhost:3306/netflix_db'
DB_URI = os.getenv('DATABASE_URI', f"sqlite:///{BASE_DIR}/netflix_etl.db")

# Input File
RAW_DATA_FILE = RAW_DATA_DIR / 'netflix_titles.csv'

# Configure Logging
LOG_FILE = LOG_DIR / 'etl_pipeline.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def get_logger(name):
    return logging.getLogger(name)
