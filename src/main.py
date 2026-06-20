import sys
from pathlib import Path
# Ensure the root directory is in the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import time
from src.config import RAW_DATA_FILE, DB_URI, get_logger
from src.extract import NetflixExtractor
from src.transform import NetflixTransformer
from src.load import NetflixLoader

logger = get_logger(__name__)

def run_etl():
    """Main execution function for the Netflix ETL pipeline."""
    start_time = time.time()
    logger.info("========================================")
    logger.info("Starting Netflix ETL Pipeline")
    logger.info("========================================")

    try:
        # 1. EXTRACT
        logger.info("\n--- PHASE 1: EXTRACT ---")
        extractor = NetflixExtractor(RAW_DATA_FILE)
        raw_df = extractor.extract()

        # 2. TRANSFORM
        logger.info("\n--- PHASE 2: TRANSFORM ---")
        transformer = NetflixTransformer(raw_df)
        transformed_df = transformer.transform()

        # 3. LOAD
        logger.info("\n--- PHASE 3: LOAD ---")
        loader = NetflixLoader(DB_URI)
        loader.load(transformed_df)

        end_time = time.time()
        logger.info("========================================")
        logger.info(f"ETL Pipeline completed successfully in {end_time - start_time:.2f} seconds.")
        logger.info("========================================")

    except Exception as e:
        logger.critical(f"ETL Pipeline failed due to an error: {e}")
        logger.exception(e)

if __name__ == "__main__":
    run_etl()
