SELECT 
city_name,
temperature,
RANK() OVER(ORDER BY temperature DESC) AS City_Rank
FROM WeatherData