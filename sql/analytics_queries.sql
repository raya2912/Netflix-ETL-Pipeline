-- SQL Analytics Queries for Netflix ETL Pipeline
-- These queries are written based on the normalized PostgreSQL/MySQL schema.
-- Note: Depending on your specific database (SQLite/PostgreSQL/MySQL), some string aggregations might slightly differ.
-- The queries below use standard ANSI SQL.

-- 1. Movies vs TV Shows distribution
SELECT 
    type, 
    COUNT(*) as total_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM content
GROUP BY type
ORDER BY total_count DESC;

-- 2. Top 10 countries producing content
SELECT 
    c.name as country, 
    COUNT(cc.show_id) as total_content
FROM country c
JOIN content_country cc ON c.id = cc.country_id
WHERE c.name != 'Unknown'
GROUP BY c.name
ORDER BY total_content DESC
LIMIT 10;

-- 3. Most common content ratings
SELECT 
    rating, 
    COUNT(*) as rating_count
FROM content
WHERE rating != 'Unknown'
GROUP BY rating
ORDER BY rating_count DESC
LIMIT 5;

-- 4. Year-wise content growth (when was content added)
SELECT 
    year_added, 
    type,
    COUNT(*) as content_count
FROM content
WHERE year_added IS NOT NULL
GROUP BY year_added, type
ORDER BY year_added ASC, type;

-- 5. Longest movies
SELECT 
    title, 
    duration,
    CAST(REPLACE(duration, ' min', '') AS UNSIGNED) as runtime_minutes -- Use CAST(REPLACE(...) AS INT) for PostgreSQL
FROM content
WHERE type = 'Movie' AND duration LIKE '% min'
ORDER BY runtime_minutes DESC
LIMIT 10;

-- 6. Most active directors
SELECT 
    d.name as director, 
    COUNT(cd.show_id) as total_titles
FROM director d
JOIN content_director cd ON d.id = cd.director_id
WHERE d.name != 'Unknown'
GROUP BY d.name
ORDER BY total_titles DESC
LIMIT 10;

-- 7. Content trends over time (release year vs year added)
SELECT 
    release_year, 
    COUNT(*) as released_count,
    SUM(CASE WHEN year_added = release_year THEN 1 ELSE 0 END) as added_same_year
FROM content
GROUP BY release_year
ORDER BY release_year DESC
LIMIT 20;
