# Netflix ETL Pipeline and Analytics System

## Project Overview
This project is an end-to-end Extract, Transform, Load (ETL) pipeline built with Python and Pandas, designed to process the Netflix Titles dataset and load it into a normalized relational database using SQLAlchemy. It is designed to showcase production-ready coding standards, Object-Oriented Programming (OOP) principles, exception handling, logging, and database modeling for a Data Engineer portfolio.

## Architecture

```mermaid
graph TD
    A[(Kaggle CSV Dataset)] -->|Extract| B(Pandas DataFrame)
    B -->|Clean & Validate| C(Transform Phase)
    C -->|Impute Nulls & Deduplicate| D{Feature Engineering}
    D -->|Derived: content_age, year_added| E(Load Phase)
    E -->|SQLAlchemy ORM| F[(Normalized SQLite/PostgreSQL)]
    
    subgraph Relational Database Schema
        F --> G[Content Fact Table]
        F --> H[Director Dimension]
        F --> I[Cast Dimension]
        F --> J[Country Dimension]
        F --> K[Category Dimension]
    end
```

1. **Extract**: Reads the raw CSV data, validating column presence.
2. **Transform**: Cleans data, handles missing values (imputes 'Unknown'), dedupes records, formats dates, and generates derived features like `content_age` and `year_added`.
3. **Load**: Maps the flat dataset into a normalized database schema with dimension tables (`director`, `country`, `category`, `cast`) to prevent data redundancy, then loads it via SQLAlchemy.

## Tech Stack
- **Python 3.10+**
- **Pandas** & **NumPy**: Data manipulation and transformation.
- **SQLAlchemy**: ORM for database connectivity and schema generation.
- **PostgreSQL / MySQL / SQLite**: Target relational databases.

## Project Structure
```text
Netflix_ETL_Pipeline/
├── data/
│   ├── raw/             # Place netflix_titles.csv here
│   └── processed/
├── logs/                # ETL execution logs are stored here
├── sql/
│   └── analytics_queries.sql
├── src/
│   ├── config.py           # Paths, DB connection, and logging setup
│   ├── database_models.py  # SQLAlchemy schema definitions
│   ├── extract.py          # Extraction logic
│   ├── transform.py        # Transformation and feature engineering logic
│   ├── load.py             # Database loading logic
│   └── main.py             # Entry point
├── requirements.txt
├── interview_prep.md       # Q&A for portfolio interviews
└── README.md
```

## How to Run the Pipeline

### 1. Prerequisites
- Python 3.9 or higher.
- A virtual environment (recommended).

### 2. Setup
1. Clone this repository and navigate to the root directory.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. **Dataset Download**: Download the [Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows) dataset from Kaggle.
5. Place the downloaded `netflix_titles.csv` file into the `data/raw/` directory.

### 3. Execution
Run the pipeline from the project root:
```bash
python src/main.py
```
*Note: By default, the application is configured in `src/config.py` to use a local SQLite database for ease of setup. A file named `netflix_etl.db` will be created in the project root.*

### 4. Database Configuration (Optional)
To use PostgreSQL or MySQL instead of SQLite, modify the `DB_URI` in `src/config.py` or set the `DATABASE_URI` environment variable:
```bash
export DATABASE_URI="postgresql://username:password@localhost:5432/netflix_db"
```

## Analytics
SQL queries for common analytical questions (e.g., top directors, movies vs tv shows ratio, longest movies) are located in `sql/analytics_queries.sql`. You can execute these against the generated database to visualize the insights.
