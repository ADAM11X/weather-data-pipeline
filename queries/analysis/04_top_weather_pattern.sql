WITH cities_by_WD as(
select 
weather_description,
count(weather_description) AS Num_of_cities
FROM WeatherData
GROUP BY weather_description
),
TOP_WD AS (
SELECT TOP 1
*
FROM cities_by_WD
ORDER BY Num_of_cities DESC
)

SELECT 
*
FROM TOP_WD