# Interview Preparation: Netflix ETL Pipeline

This document contains potential interview questions and suggested answers related to the Netflix ETL Pipeline project on your resume.

## Q1: Explain the architecture of your Netflix ETL pipeline.
**A:** The architecture is a classic batch ETL pipeline built entirely in Python.
- **Extract:** The raw Netflix dataset (CSV format) is ingested using Pandas. I implemented basic validation checks to ensure all required columns exist before processing.
- **Transform:** In the transformation layer, I used Pandas to handle missing values (imputing 'Unknown' for categorical dimensions), removed duplicates based on `show_id`, standardized text fields, converted string dates to datetime objects, and engineered new features like `content_age` and `year_added`.
- **Load:** The clean data is then loaded into a relational database. I used SQLAlchemy as the ORM to automatically map and push the Pandas dataframes to a normalized database schema. 

## Q2: Why did you normalize the database schema instead of just dumping the flat CSV file into a single SQL table?
**A:** The raw dataset contains comma-separated values in fields like `director`, `cast`, `country`, and `listed_in`. Dumping this as a flat table violates First Normal Form (1NF) and makes analytical queries (like "Find the top 10 most active directors") extremely inefficient because it would require string matching (`LIKE '%Director%'`) instead of simple JOINs. By normalizing the schema into dimension tables and junction/mapping tables, we improve query performance, enforce data integrity, and adhere to proper data warehousing practices.

## Q3: How did you handle missing values or dirty data?
**A:** I took a targeted approach depending on the column's criticality. For essential fields like `title` and `date_added`, I dropped the records because the data was practically useless for time-based analytics without them. For dimensional fields like `director` or `country`, I imputed the missing values with the string 'Unknown'. This allowed me to keep the core content record intact while handling the missing dimensions cleanly in the database schema.

## Q4: How did you handle database inserts? What if a record already existed?
**A:** To simulate an incremental load and avoid Primary Key constraint violations, I queried the database for the `show_id` before inserting a new row. If it existed, the record was skipped. In a true production environment with massive data volumes, I would likely use bulk upserts (`ON CONFLICT DO UPDATE` in PostgreSQL or `INSERT ... ON DUPLICATE KEY UPDATE` in MySQL) to update existing records more efficiently. 

## Q5: How did you make your code production-ready?
**A:** I applied several software engineering best practices:
1. **OOP (Object-Oriented Programming):** I abstracted the Extract, Transform, and Load logic into dedicated classes (`NetflixExtractor`, `NetflixTransformer`, `NetflixLoader`), making the code modular and easy to test.
2. **Logging:** Instead of `print()` statements, I used Python's `logging` module to track execution steps and record errors to a log file (`logs/etl_pipeline.log`).
3. **Configuration Management:** I decoupled configuration (database URIs, file paths) from the logic by centralizing it in `config.py`.
4. **Exception Handling:** I wrapped critical I/O operations (reading CSV, connecting to the DB) in `try-except` blocks so the pipeline fails gracefully and logs the stack trace if an issue occurs.
