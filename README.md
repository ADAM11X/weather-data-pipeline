# Weather Data Pipeline

A data engineering project that extracts current weather data from the OpenWeather API, transforms it, and loads it into SQL Server for analytical querying.

## Overview

This project demonstrates a complete **ETL (Extract, Transform, Load)** pipeline:

**OpenWeather API → Python → SQL Server → SQL Analysis**

The pipeline fetches current weather data for 60 cities worldwide, cleans and structures the API responses, loads the data into a relational database, and runs analytical SQL queries.

## Technologies Used

* Python
* Requests
* pyodbc
* SQL Server
* SQL
* Git
* GitHub

## Project Structure

```text
weather-data-pipeline/

├── config/
│   └── cities.json                    # List of 60 cities to track
│
├── src/
│   ├── extract.py                     # Fetch data from OpenWeather API
│   ├── transform.py                   # Clean and structure API responses
│   └── load.py                        # Insert data into SQL Server
│
├── queries/
│   ├── analysis/
│   │   ├── 01_avg_temp_by_city.sql    # Average temperature by city
│   │   ├── 02_hottest_city.sql        # City with highest temperature
│   │   ├── 03_city_temp_ranking.sql   # Temperature ranking
│   │   └── 04_top_weather_pattern.sql # Most common weather condition
│   │
│   └── CDC/
│       ├── setup_cdc.sql               # Enables SQL Server CDC
│       └── get_changes.sql             # Queries captured changes
│
├── schema.sql                          # Database and table creation
├── run_pipeline.py                     # Main ETL entry point
├── requirements.txt                    # Python dependencies
├── .env.example                        # API key template
├── .gitignore                          # Excludes sensitive/local files
└── README.md                           # Project documentation
```

## Dataset

* **Source:** OpenWeather API
* **Coverage:** 60 cities worldwide
* **Data:** Current weather conditions fetched at runtime
* **Fields:**

  * City name
  * Country code
  * Timestamp
  * Temperature
  * Feels-like temperature
  * Humidity
  * Wind speed
  * Weather description

## Database

* **Server:** SQL Server
* **Database:** `WeatherDataDB`
* **Table:** `WeatherData`

## ETL Pipeline

### 1. Extract

The extraction stage:

* Reads the city list from `config/cities.json`
* Calls the OpenWeather API for each city
* Processes API responses in JSON format
* Handles common API errors such as:

  * Network failures
  * City not found
  * Rate limits
  * Invalid API keys

The extracted data is passed to the transformation stage.

### 2. Transform

The transformation stage:

* Extracts the required fields from the nested JSON responses
* Converts Unix timestamps into datetime values
* Handles missing values
* Structures the data into clean records ready for database insertion

### 3. Load

The loading stage:

* Connects to SQL Server using `pyodbc`
* Clears the existing table before loading the latest dataset
* Inserts records using `fast_executemany`
* Uses a database transaction to maintain consistency
* Rolls back the operation if an error occurs
* Safely closes database resources
* Returns the number of successfully loaded rows

The current pipeline uses a **full clear-and-reload strategy**.

## SQL Analysis

The project includes analytical SQL queries covering aggregation, ranking, window functions, and CTEs.

| # | File                                  | Question                                   | Concepts                 |
| - | ------------------------------------- | ------------------------------------------ | ------------------------ |
| 1 | `analysis/01_avg_temp_by_city.sql`    | What is the average temperature by city?   | `GROUP BY`, `AVG`        |
| 2 | `analysis/02_hottest_city.sql`        | Which city has the highest temperature?    | `TOP`, `ORDER BY`        |
| 3 | `analysis/03_city_temp_ranking.sql`   | How are cities ranked by temperature?      | `RANK`, Window Functions |
| 4 | `analysis/04_top_weather_pattern.sql` | What is the most common weather condition? | CTE, `COUNT`             |

## Change Data Capture (CDC) — Experimental

The `queries/CDC/` directory contains SQL Server CDC scripts created to explore **incremental change tracking** as an alternative to the current full reload strategy.

The scripts demonstrate:

* Enabling CDC on the `WeatherData` table
* Working with CDC capture instances
* Querying captured changes
* Using LSNs (Log Sequence Numbers)
* Using a watermark to identify previously processed changes

### Current Status

CDC is **not yet integrated into the Python ETL pipeline**.

The current `run_pipeline.py` execution still performs a full clear-and-reload.

The CDC scripts currently work as standalone SQL Server experiments. Integrating CDC-based change processing into the Python pipeline is planned for a future version.

This distinction is intentional: CDC is documented as an **experimental component**, not as a completed pipeline feature.

## How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure the API Key

Copy `.env.example` to `.env` and add your OpenWeather API key:

```env
OPENWEATHER_API_KEY=your_key_here
```

The `.env` file is excluded from Git using `.gitignore`.

### 3. Create the Database

Run `schema.sql` in SQL Server.

This creates:

```text
WeatherDataDB
└── WeatherData
```

### 4. Run the Pipeline

From the project root:

```bash
python run_pipeline.py
```

The pipeline will:

```text
Read cities
    ↓
Call OpenWeather API
    ↓
Extract JSON data
    ↓
Transform data
    ↓
Connect to SQL Server
    ↓
Load WeatherData
```

### 5. Run the SQL Analysis

Execute the queries located in:

```text
queries/analysis/
```

against the `WeatherDataDB` database.

## What This Project Demonstrates

* Building an ETL pipeline with Python
* Consuming a REST API
* Working with JSON data
* Data transformation and cleaning
* SQL Server database integration
* Transaction management and rollback
* Safe database resource handling
* Error handling
* Analytical SQL
* Window functions
* Common Table Expressions (CTEs)
* SQL Server Change Data Capture concepts
* LSN-based watermarking
* Environment variable management
* Git version control
* Feature branching
* Fast-forward merges
* Git tagging

## Roadmap

* [ ] Integrate CDC-based change processing into the Python pipeline
* [ ] Add retry logic for OpenWeather API requests
* [ ] Replace `print` statements with structured logging
* [ ] Add automated data quality checks
* [ ] Schedule pipeline execution with Apache Airflow

## Versioning

### V1 — Initial Pipeline

Initial working version containing:

* API extraction
* Data transformation
* SQL Server loading
* SQL analysis queries

### V1.1 — Refactor & CDC Exploration

Added:

* Reorganized SQL queries into `analysis/` and `CDC/`
* SQL Server CDC exploration scripts
* Transaction safety in `load.py`
* Improved project structure and documentation

> CDC integration with the Python pipeline is not part of V1.1.

## Author

**ADAM11X**

GitHub: https://github.com/ADAM11X
