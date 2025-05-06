from dagster import job, op
import os
from dotenv import load_dotenv
from datetime import datetime
import requests
import csv
import duckdb
import pandas as pd

load_dotenv()

@op
def get_cities():
    return ["jakarta", "new york", "london", "beijing", "singapore"]

@op
def fetch_aqi_data(cities):
    token = os.getenv("WAQI_API_KEY")
    results = []
    for city in cities:
        url = f"https://api.waqi.info/feed/{city}/?token={token}"
        try:
            response = requests.get(url)
            data = response.json()
            if data.get('status') == 'ok':
                results.append({
                    "city": city,
                    "aqi": data['data'].get('aqi', 'N/A'),
                    "dominant": data['data'].get('dominentpol', 'N/A'),
                    "timestamp": data['data']['time'].get('iso', 'N/A'),
                    "pm25": data['data']['iaqi'].get('pm25', {}).get('v', 'N/A')
                })
        except Exception as e:
            print(f"Failed for {city}: {e}")
    return results

@op
def save_to_csv(data):
    now = datetime.now()
    filename = f"aq{now.strftime('%Y%m%d%H%M%S')}.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["City", "AQI", "Dominant Pollutant", "PM2.5", "Timestamp"])
        for row in data:
            writer.writerow([row["city"], row["aqi"], row["dominant"], row["pm25"], row["timestamp"]])

@op
def save_to_duckdb(data):
    df = pd.DataFrame(data)
    df = df[["city", "aqi", "dominant", "timestamp", "pm25"]]
    df["aqi"] = pd.to_numeric(df["aqi"], errors="coerce")
    df["pm25"] = pd.to_numeric(df["pm25"], errors="coerce")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    
    db_path = os.path.join(os.path.dirname(__file__), "../../../aqi_data.duckdb")
    conn = duckdb.connect(database=db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS aqi_data (
            city TEXT,
            aqi INTEGER,
            dominant TEXT,
            timestamp TIMESTAMP,
            pm25 DOUBLE
        )
    """)
    conn.register("df", df)
    conn.execute("INSERT INTO aqi_data SELECT city, aqi, dominant, timestamp, pm25 FROM df")
    conn.close()

    
@job
def aq_job():
    cities = get_cities()
    data = fetch_aqi_data(cities)
    save_to_csv(data)
    save_to_duckdb(data)