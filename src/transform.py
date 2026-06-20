import pandas as pd
from datetime import datetime
from src.config import get_logger

logger = get_logger(__name__)

class NetflixTransformer:
    """
    Class responsible for transforming the raw Netflix dataset.
    This includes cleaning, handling nulls, and generating derived features.
    """
    def __init__(self, df: pd.DataFrame):
        # Working on a copy to preserve immutability where possible
        self.df = df.copy()

    def clean_missing_values(self):
        """Handles missing values in critical columns."""
        initial_len = len(self.df)
        
        # Drop records without a title or date_added (critical for our analysis)
        self.df.dropna(subset=['title', 'date_added'], inplace=True)
        
        # Fill missing dimensional data with 'Unknown'
        fill_cols = ['director', 'cast', 'country', 'rating']
        for col in fill_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna('Unknown')
                
        logger.info(f"Dropped {initial_len - len(self.df)} rows due to critical missing values.")

    def format_dates(self):
        """Formats the date_added column and creates year_added."""
        try:
            # Strip whitespace and convert to datetime
            self.df['date_added'] = self.df['date_added'].str.strip()
            self.df['date_added'] = pd.to_datetime(self.df['date_added'], format='mixed')
            
            # Extract year_added
            self.df['year_added'] = self.df['date_added'].dt.year
        except Exception as e:
            logger.error(f"Error formatting dates: {e}")
            raise

    def create_derived_features(self):
        """Calculates derived features like content_age."""
        current_year = datetime.now().year
        self.df['content_age'] = current_year - self.df['release_year']
        logger.info("Derived features 'year_added' and 'content_age' created.")

    def standardize_text(self):
        """Standardizes text fields by removing extra spaces."""
        text_cols = ['title', 'director', 'cast', 'country', 'listed_in']
        for col in text_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str).str.strip()

    def deduplicate(self):
        """Removes duplicate rows based on show_id."""
        initial_len = len(self.df)
        self.df.drop_duplicates(subset=['show_id'], keep='first', inplace=True)
        dupes = initial_len - len(self.df)
        if dupes > 0:
            logger.info(f"Removed {dupes} duplicate rows.")

    def transform(self) -> pd.DataFrame:
        """Executes the full transformation pipeline."""
        logger.info("Starting transformation phase...")
        self.deduplicate()
        self.clean_missing_values()
        self.standardize_text()
        self.format_dates()
        self.create_derived_features()
        logger.info("Transformation phase complete.")
        return self.df
