# ETL Data Pipeline for Air Quality Index

An automated ETL pipeline built with [Dagster](https://dagster.io/) to extract and store Air Quality Index (AQI) data from [https://waqi.info](https://waqi.info) via API.

This project fetches air quality data and stores it locally in both `.csv` and [DuckDB](https://duckdb.org/) formats for easy access and analysis.

---

## Features

### ETL Pipeline

Built using the **Dagster** orchestration framework:

1. **Extract**: Pull real-time AQI data via the [WAQI API](https://aqicn.org/api/).
2. **Transform**: Normalize and enrich the raw API response to a tabular format suitable for downstream analytics. This includes:

   * Flattening nested JSON structures
   * Renaming fields
   * Standardizing timestamps
3. **Load**: Save the processed data to:

   * Local **DuckDB** database
   * **CSV** file for external usage or backup

---

### Project Structure

```
aqi-etl/
├── .env                         # Environment variables (API token, paths)
├── README.md                    # Project documentation
├── run_aqapi2.ps1               # PowerShell script to run ETL via Task Scheduler
├── aqapi2.py                    # Python script for AQI extraction and loading
├── dagster_project/
│   ├── pyproject.toml           # Dagster project dependencies
│   ├── dagster_project/
│   │   ├── __init__.py
│   │   ├── repository.py        # Registering Dagster jobs and schedules
│   │   ├── jobs/
│   │   │   └── aq_job.py        # Dagster job for ETL
│   │   ├── schedules/
│   │   │   └── aq_schedule.py   # Dagster schedule (optional)
│   │   └── sensors/             # Placeholder for Dagster sensors
│   └── workspace.yaml
└── requirements.txt             # Python dependencies
```

---

## Local Automation (Windows)

The ETL can also run independently of Dagster using **Windows Task Scheduler**, ideal for daily data collection.

### Scripts

1. `aqapi2.py`: Fetches AQI data and stores it to CSV and DuckDB.
2. `run_aqapi2.ps1`: Activates the Conda environment and runs `aqapi2.py`.

### Setup Windows Task Scheduler

1. Open **Task Scheduler**
2. Click **Create Basic Task**
3. **Name**: `Run AQ API`
4. **Trigger**: Daily at 8:00 AM
5. **Action**: Start a program
6. **Program/script**: `powershell.exe`
7. **Add arguments**:

   ```
   -ExecutionPolicy Bypass -File "C:\path\to\your\run_aqapi2.ps1"
   ```
8. **Conditions**: Uncheck "Start only if the computer is on AC power" (especially for laptops).
9. **General**:

   * Check “Run whether user is logged on or not”
   * Check “Run with highest privileges”


