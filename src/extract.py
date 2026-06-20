import pandas as pd
from pathlib import Path
from typing import Tuple
from src.config import get_logger

logger = get_logger(__name__)

class NetflixExtractor:
    """
    Class responsible for extracting data from the raw CSV source.
    """
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def validate_file(self) -> bool:
        """Validates if the raw file exists."""
        if not self.file_path.exists():
            logger.error(f"File not found: {self.file_path}")
            return False
        return True

    def extract(self) -> pd.DataFrame:
        """
        Extracts the data into a pandas DataFrame.
        Returns an empty DataFrame if extraction fails.
        """
        logger.info(f"Starting extraction from {self.file_path}")
        try:
            if not self.validate_file():
                raise FileNotFoundError(f"Missing file: {self.file_path}")
            
            df = pd.read_csv(self.file_path)
            
            # Basic validation
            expected_columns = ['show_id', 'type', 'title', 'director', 'cast', 'country', 
                                'date_added', 'release_year', 'rating', 'duration', 'listed_in', 'description']
            
            missing_cols = [col for col in expected_columns if col not in df.columns]
            if missing_cols:
                logger.warning(f"Missing expected columns in source: {missing_cols}")
            
            logger.info(f"Successfully extracted {len(df)} records.")
            return df
            
        except Exception as e:
            logger.error(f"Error during extraction: {e}")
            raise
