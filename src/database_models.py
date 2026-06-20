from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Content(Base):
    """Core Fact Table for Netflix Content."""
    __tablename__ = 'content'

    show_id = Column(String(50), primary_key=True)
    type = Column(String(50), index=True) # Movie or TV Show
    title = Column(String(500), nullable=False)
    release_year = Column(Integer, index=True)
    rating = Column(String(50))
    duration = Column(String(100))
    date_added = Column(Date)
    year_added = Column(Integer)
    content_age = Column(Integer)
    description = Column(Text)

class Director(Base):
    """Dimension Table for Directors."""
    __tablename__ = 'director'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

class ContentDirector(Base):
    """Mapping Table resolving Many-to-Many between Content and Director."""
    __tablename__ = 'content_director'

    show_id = Column(String(50), ForeignKey('content.show_id'), primary_key=True)
    director_id = Column(Integer, ForeignKey('director.id'), primary_key=True)

class Country(Base):
    """Dimension Table for Countries."""
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

class ContentCountry(Base):
    """Mapping Table for Content and Country."""
    __tablename__ = 'content_country'

    show_id = Column(String(50), ForeignKey('content.show_id'), primary_key=True)
    country_id = Column(Integer, ForeignKey('country.id'), primary_key=True)

class Category(Base):
    """Dimension Table for Categories (listed_in)."""
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

class ContentCategory(Base):
    """Mapping Table for Content and Category."""
    __tablename__ = 'content_category'

    show_id = Column(String(50), ForeignKey('content.show_id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'), primary_key=True)

class CastMember(Base):
    """Dimension Table for Cast."""
    __tablename__ = 'cast_member'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

class ContentCast(Base):
    """Mapping Table for Content and Cast."""
    __tablename__ = 'content_cast'

    show_id = Column(String(50), ForeignKey('content.show_id'), primary_key=True)
    cast_id = Column(Integer, ForeignKey('cast_member.id'), primary_key=True)

def init_db(db_uri):
    """Initialize the database and create tables if they don't exist."""
    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)
    return engine
