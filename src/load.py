import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.database_models import Content, Director, ContentDirector, Country, ContentCountry, Category, ContentCategory, CastMember, ContentCast, init_db
from src.config import get_logger

logger = get_logger(__name__)

class NetflixLoader:
    """
    Class responsible for loading transformed data into the relational database.
    """
    def __init__(self, db_uri: str):
        self.engine = init_db(db_uri)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Simple caches to minimize DB queries for dimensions
        self._director_cache = {}
        self._country_cache = {}
        self._category_cache = {}
        self._cast_cache = {}

    def _get_or_create_dimension(self, model, cache: dict, name: str):
        """Helper to get an existing dimension record or create a new one."""
        if not name:
            return None
            
        name = name.strip()
        if name in cache:
            return cache[name]

        instance = self.session.query(model).filter_by(name=name).first()
        if not instance:
            instance = model(name=name)
            self.session.add(instance)
            self.session.commit() # Commit to get ID
            
        cache[name] = instance
        return instance

    def load(self, df: pd.DataFrame):
        """Loads the dataframe into the normalized database schema."""
        logger.info("Starting load phase...")
        try:
            records_inserted = 0
            
            for index, row in df.iterrows():
                # Check if content already exists
                existing_content = self.session.query(Content).filter_by(show_id=row['show_id']).first()
                if existing_content:
                    continue # Skip to implement basic incremental load

                # Create core content record
                content = Content(
                    show_id=row['show_id'],
                    type=row['type'],
                    title=row['title'],
                    release_year=row['release_year'],
                    rating=row['rating'],
                    duration=row['duration'],
                    date_added=row['date_added'] if pd.notnull(row['date_added']) else None,
                    year_added=row['year_added'] if pd.notnull(row['year_added']) else None,
                    content_age=row['content_age'] if pd.notnull(row['content_age']) else None,
                    description=row['description']
                )
                self.session.add(content)

                # Process Directors
                if pd.notnull(row['director']) and row['director'] != 'Unknown':
                    directors = set([d.strip() for d in row['director'].split(',') if d.strip()])
                    for d_name in directors:
                        d_obj = self._get_or_create_dimension(Director, self._director_cache, d_name)
                        if d_obj:
                            self.session.add(ContentDirector(show_id=content.show_id, director_id=d_obj.id))

                # Process Countries
                if pd.notnull(row['country']) and row['country'] != 'Unknown':
                    countries = set([c.strip() for c in row['country'].split(',') if c.strip()])
                    for c_name in countries:
                        c_obj = self._get_or_create_dimension(Country, self._country_cache, c_name)
                        if c_obj:
                            self.session.add(ContentCountry(show_id=content.show_id, country_id=c_obj.id))

                # Process Cast
                if pd.notnull(row['cast']) and row['cast'] != 'Unknown':
                    cast_members = set([c.strip() for c in row['cast'].split(',') if c.strip()])
                    for cast_name in cast_members:
                        cast_obj = self._get_or_create_dimension(CastMember, self._cast_cache, cast_name)
                        if cast_obj:
                            self.session.add(ContentCast(show_id=content.show_id, cast_id=cast_obj.id))

                # Process Categories (listed_in)
                if pd.notnull(row['listed_in']) and row['listed_in'] != 'Unknown':
                    categories = set([cat.strip() for cat in row['listed_in'].split(',') if cat.strip()])
                    for cat_name in categories:
                        cat_obj = self._get_or_create_dimension(Category, self._category_cache, cat_name)
                        if cat_obj:
                            self.session.add(ContentCategory(show_id=content.show_id, category_id=cat_obj.id))

                records_inserted += 1
                
                # Commit in batches of 500
                if records_inserted % 500 == 0:
                    self.session.commit()
                    logger.info(f"Loaded {records_inserted} records...")

            # Final commit
            self.session.commit()
            logger.info(f"Load phase complete. Inserted {records_inserted} new content records.")
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error during load phase: {e}")
            raise
        finally:
            self.session.close()
