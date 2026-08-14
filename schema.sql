CREATE DATABASE WeatherDataDB;
GO

USE WeatherDataDB;
GO

CREATE TABLE WeatherData (
	ID INT  IDENTITY(1,1) PRIMARY KEY,
	country_name VARCHAR(30),
	country_code CHAR(3) NOT NULL,
	timestamp	DATETIME ,
	temperature	DECIMAL(10,2) NOT NULL,
	feels_like DECIMAL(10,2) ,
	humidity INT NOT NULL,
	wind_speed DECIMAL(10,2) ,
	weather_description	VARCHAR(40) 
);