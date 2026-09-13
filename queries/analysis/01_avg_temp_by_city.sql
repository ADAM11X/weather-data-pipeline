SELECT 
city_name,
CAST(AVG(temperature)AS decimal(5,2)) AS AVG_Temp
FROM WeatherData
GROUP BY city_name
ORDER BY AVG_Temp