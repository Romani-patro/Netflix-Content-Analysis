USE netflix_analysis;

-- 1. Total Netflix content
SELECT COUNT(*) AS total_content
FROM netflix;

-- 2. Movies vs TV Shows
SELECT
    type,
    COUNT(*) AS total
FROM netflix
GROUP BY type
ORDER BY total DESC;

-- 3. Latest release years
SELECT
    release_year,
    COUNT(*) AS total
FROM netflix
GROUP BY release_year
ORDER BY release_year DESC
LIMIT 10;
-- 4. Top 10 countries by Netflix content
SELECT
    country,
    COUNT(*) AS total_content
FROM netflix
WHERE country IS NOT NULL
  AND country <> 'Unknown'
GROUP BY country
ORDER BY total_content DESC
LIMIT 10;
-- 5. Netflix content added by year
SELECT
    YEAR(date_added) AS year_added,
    COUNT(*) AS total_content
FROM netflix
WHERE date_added IS NOT NULL
GROUP BY YEAR(date_added)
ORDER BY year_added;
-- 6. Top 10 Netflix genres
WITH RECURSIVE genre_split AS (
    SELECT
        TRIM(SUBSTRING_INDEX(listed_in, ',', 1)) AS genre,
        CASE
            WHEN listed_in LIKE '%,%'
            THEN SUBSTRING(listed_in, LOCATE(',', listed_in) + 1)
            ELSE ''
        END AS remaining
    FROM netflix
    WHERE listed_in IS NOT NULL
      AND listed_in <> 'Unknown'

    UNION ALL

    SELECT
        TRIM(SUBSTRING_INDEX(remaining, ',', 1)),
        CASE
            WHEN remaining LIKE '%,%'
            THEN SUBSTRING(remaining, LOCATE(',', remaining) + 1)
            ELSE ''
        END
    FROM genre_split
    WHERE remaining <> ''
)
SELECT
    genre,
    COUNT(*) AS total_content
FROM genre_split
WHERE genre <> ''
GROUP BY genre
ORDER BY total_content DESC
LIMIT 10;
-- 7. Netflix content by rating
SELECT
    rating,
    COUNT(*) AS total_content
FROM netflix
WHERE rating IS NOT NULL
  AND rating <> 'Unknown'
GROUP BY rating
ORDER BY total_content DESC;
-- 8. Average movie duration in minutes
SELECT
    ROUND(AVG(CAST(SUBSTRING_INDEX(duration, ' ', 1) AS UNSIGNED)), 2)
    AS average_movie_duration
FROM netflix
WHERE type = 'Movie'
  AND duration LIKE '%min';
  -- 9. TV Shows by number of seasons
SELECT
    duration,
    COUNT(*) AS total_shows
FROM netflix
WHERE type = 'TV Show'
  AND duration LIKE '%Season%'
GROUP BY duration
ORDER BY total_shows DESC;
-- 10. Top 10 directors on Netflix
SELECT
    director,
    COUNT(*) AS total_titles
FROM netflix
WHERE director IS NOT NULL
  AND director <> 'Unknown'
GROUP BY director
ORDER BY total_titles DESC
LIMIT 10;