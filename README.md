# Weather Data Pipeline

A data engineering project that extracts current weather data from the OpenWeather API, transforms it with Python, and loads it into SQL Server for analytical querying.

## Overview

This project implements an ETL (Extract, Transform, Load) pipeline:

**OpenWeather API → Python → SQL Server → SQL Analysis**

The pipeline fetches current weather data for 60 cities worldwide, transforms the API responses into structured records, loads the data into SQL Server, and provides SQL queries for analysis.

The project also includes Python logging for pipeline execution monitoring and an experimental SQL Server CDC component that is currently not integrated into the main ETL workflow.

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
│   └── load.py                        # Load data into SQL Server
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
├── logs/
│   └── pipeline.log                    # Pipeline execution logs
│
├── schema.sql                          # Database and table creation
├── run_pipeline.py                     # Main ETL entry point and logging configuration
├── requirements.txt                    # Python dependencies
├── .env.example                        # API key template
├── .gitignore                          # Excludes sensitive and local files
└── README.md                           # Project documentation
```

The `logs/` directory is excluded from Git. Log files remain local to the environment where the pipeline is executed.

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

The pipeline loads transformed weather data into Microsoft SQL Server.

* **Server:** SQL Server
* **Database:** `WeatherDataDB`
* **Table:** `WeatherData`

The current pipeline uses a **full clear-and-reload strategy**. Each execution clears the existing data and loads the latest weather dataset.

## ETL Pipeline

### Extract

The extraction stage:

* Reads the list of cities from `config/cities.json`
* Sends requests to the OpenWeather API
* Retrieves weather data in JSON format
* Handles API and request errors such as:

  * Network failures
  * City not found
  * Rate limits
  * Invalid API keys

The extracted API responses are passed to the transformation stage.

### Transform

The transformation stage:

* Extracts the required fields from the nested JSON responses
* Converts Unix timestamps into datetime values
* Handles missing values
* Structures the data into records suitable for SQL Server

### Load

The loading stage:

* Connects to SQL Server using `pyodbc`
* Clears the existing `WeatherData` table
* Inserts the transformed records using `fast_executemany`
* Uses a database transaction to maintain consistency
* Rolls back the transaction if an error occurs
* Safely closes database resources
* Reports the number of successfully loaded rows

The current implementation does not perform incremental loading.

## Logging

The pipeline uses Python's built-in `logging` module to record execution events.

Logging is configured in `run_pipeline.py`, while other modules use Python loggers to write messages during their execution.

Logs are written to:

```text
logs/pipeline.log
```

The log file uses **append mode**, so logs from previous pipeline executions are preserved instead of being overwritten.

The `logs/` directory is excluded from Git because pipeline logs are runtime-generated local files.

This provides basic execution monitoring without introducing a separate logging framework or structured logging format.

## SQL Analysis

The project includes SQL queries for analyzing the weather data stored in SQL Server.

| # | File                                  | Question                                   | Concepts                 |
| - | ------------------------------------- | ------------------------------------------ | ------------------------ |
| 1 | `analysis/01_avg_temp_by_city.sql`    | What is the average temperature by city?   | `GROUP BY`, `AVG`        |
| 2 | `analysis/02_hottest_city.sql`        | Which city has the highest temperature?    | `TOP`, `ORDER BY`        |
| 3 | `analysis/03_city_temp_ranking.sql`   | How are cities ranked by temperature?      | `RANK`, Window Functions |
| 4 | `analysis/04_top_weather_pattern.sql` | What is the most common weather condition? | CTE, `COUNT`             |

These queries demonstrate common SQL analysis techniques including aggregation, sorting, window functions, and Common Table Expressions.

## Change Data Capture (CDC) — Experimental

The `queries/CDC/` directory contains SQL Server CDC scripts created to explore **Change Data Capture and incremental change processing**.

The scripts demonstrate:

* Enabling CDC on the `WeatherData` table
* Working with CDC capture instances
* Querying captured changes
* Working with LSNs (Log Sequence Numbers)
* Using a watermark to identify previously processed changes

### Current Status

CDC is **not integrated into the Python ETL pipeline**.

The current pipeline still uses a full clear-and-reload strategy:

```text
OpenWeather API
      ↓
Python ETL
      ↓
Clear WeatherData
      ↓
Load latest data
```

The CDC scripts currently serve as standalone SQL Server experiments. They are not part of the production execution path of `run_pipeline.py`.

CDC integration is planned as a future improvement and should not be considered a completed feature of the current pipeline.

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/ADAM11X/weather-data-pipeline.git
cd weather-data-pipeline
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the API Key

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Then add your OpenWeather API key:

```env
OPENWEATHER_API_KEY=your_key_here
```

The `.env` file is excluded from Git.

### 4. Create the Database

Run `schema.sql` in SQL Server.

This creates:

```text
WeatherDataDB
└── WeatherData
```

### 5. Run the Pipeline

From the project root:

```bash
python run_pipeline.py
```

The pipeline executes the following flow:

```text
Read cities
    ↓
Call OpenWeather API
    ↓
Extract JSON responses
    ↓
Transform weather data
    ↓
Connect to SQL Server
    ↓
Clear existing data
    ↓
Load transformed data
    ↓
Write execution logs
```

### 6. Check the Logs

After execution, pipeline logs are available at:

```text
logs/pipeline.log
```

The log file is appended to on each execution, preserving previous pipeline runs.

### 7. Run the SQL Analysis

Execute the SQL files located in:

```text
queries/analysis/
```

against the `WeatherDataDB` database.

## What This Project Demonstrates

* Building an ETL pipeline with Python
* Consuming a REST API
* Working with JSON data
* Data transformation and cleaning
* SQL Server integration with `pyodbc`
* Bulk-oriented inserts with `fast_executemany`
* Database transaction management
* Rollback handling
* Error handling
* Python application logging
* Log persistence using append mode
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

## Versioning

### V1 — Initial Pipeline

Initial working version containing:

* OpenWeather API extraction
* Python data transformation
* SQL Server loading
* SQL analysis queries

### V1.1 — Refactor & CDC Exploration

Added:

* Reorganized SQL queries into `analysis/` and `CDC/`
* SQL Server CDC exploration scripts
* Transaction safety in `load.py`
* Python logging
* Persistent append-mode pipeline logs
* Improved project structure and documentation

> CDC integration with the Python pipeline is not part of V1.1.

## Author

**ADAM11X**

GitHub: https://github.com/ADAM11X
