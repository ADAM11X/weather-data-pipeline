 
# Weather Data Pipeline

A data engineering project that extracts real-time weather data from the OpenWeather API, transforms it, and loads it into SQL Server for analytical querying.

## Overview

This project demonstrates a complete ETL (Extract, Transform, Load) pipeline:

**OpenWeather API → Python → SQL Server → SQL Analysis**

The pipeline fetches current weather data for 60 cities worldwide, cleans and structures the data, loads it into a relational database, and runs analytical SQL queries.

## Technologies Used

- Python
- Requests
- pyodbc
- SQL Server
- SQL
- Git
- GitHub

## Project Structure

```
weather-data-pipeline/
├── config/
│   └── cities.json              # List of 60 cities to track
├── src/
│   ├── extract.py               # Fetch data from OpenWeather API
│   ├── transform.py             # Clean and structure API responses
│   └── load.py                  # Insert data into SQL Server
├── queries/
│   ├── 01_avg_temp_by_city.sql  # Average temperature by city
│   ├── 02_hottest_city.sql      # City with highest temperature
│   ├── 03_city_temp_ranking.sql # Temperature ranking with window function
│   └── 04_top_weather_pattern.sql # Most common weather (CTE)
├── schema.sql                   # Database table creation
├── run_pipeline.py              # Main script: runs full ETL
├── requirements.txt             # Python dependencies
├── .env.example                 # API key template
├── .gitignore                   # Excludes .env and data files
└── README.md                    # This file
```

## Dataset

- **Source:** OpenWeather API (free tier)
- **Coverage:** 60 cities worldwide
- **Fields:** city name, country code, timestamp, temperature, feels like, humidity, wind speed, weather description
- **Update frequency:** Real-time (current weather)

## Database

- **Server:** SQL Server (localhost)
- **Database:** WeatherDataDB
- **Table:** WeatherData

## ETL Pipeline

### Extract
- Reads city list from `config/cities.json`
- Calls OpenWeather API for each city
- Handles errors: network failures, city not found, rate limits, invalid API key
- Returns raw JSON responses

### Transform
- Extracts relevant fields from JSON
- Converts Unix timestamp to datetime
- Handles missing values with defaults
- Returns clean list of dictionaries

### Load
- Connects to SQL Server using pyodbc
- Truncates existing data
- Inserts new rows using fast_executemany
- Returns row count

## SQL Queries

| # | File | Question | Concepts |
|---|------|----------|----------|
| 1 | 01_avg_temp_by_city.sql | Average temperature by city | GROUP BY, AVG |
| 2 | 02_hottest_city.sql | City with highest temperature | TOP, ORDER BY |
| 3 | 03_city_temp_ranking.sql | All cities ranked by temperature | RANK, window function |
| 4 | 04_top_weather_pattern.sql | Most common weather condition | CTE, COUNT |

## How to Run

### 1. Install dependencies

pip install -r requirements.txt


### 2. Configure API key
Copy `.env.example` to `.env` and add your OpenWeather API key:

OPENWEATHER_API_KEY=your_key_here


### 3. Create database
Run `schema.sql` in SQL Server to create the `WeatherDataDB` database and `WeatherData` table.

### 4. Run the pipeline

python run_pipeline.py


### 5. Run queries
Execute the SQL files in `queries/` against the `WeatherDataDB` database.

## What This Project Demonstrates

- Building an ETL pipeline with Python
- Working with REST APIs and JSON data
- Database design and SQL Server integration
- Error handling and logging
- Analytical SQL with window functions and CTEs
- Environment variable management
- Git version control

## Author

**ADAM11X**

GitHub: https://github.com/ADAM11X
