import requests
import csv
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API token from environment variables
api_token = os.getenv("WAQI_API_KEY")

def get_aqi(city, token):
    """
    Fetches real-time AQI data for a specific city.

    Parameters:
        city (str): The name of the city (e.g., 'New York', 'Beijing').
        token (str): Your AQICN API token.

    Returns:
        dict: The AQI data as a dictionary or None if an error occurs.
    """
    url = f"https://api.waqi.info/feed/{city}/?token={token}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        if data.get('status') == 'ok':
            return data
        else:
            print(f"Error: {data.get('data')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred for {city}: {e}")
        return None


def save_aqi_to_csv(city_list, token):
    """
    Fetch AQI data for multiple cities and save it to a CSV file.

    Parameters:
        city_list (list): A list of city names.
        token (str): Your AQICN API token.
    """
    # Get the current date and time for the filename
    now = datetime.now()
    filename = f"aq{now.strftime('%Y%m%d%H%M%S')}.csv"

    # Prepare CSV file
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Write header
        writer.writerow(['Date', 'City', 'AQI', 'Dominant Pollutant', 'PM2.5 Value', 'Timestamp'])

        # Process each city
        for city in city_list:
            aqi_data = get_aqi(city, token)
            if aqi_data:
                city_name = aqi_data['data']['city'].get('name', 'N/A')
                aqi = aqi_data['data'].get('aqi', 'N/A')
                dominant_pollutant = aqi_data['data'].get('dominentpol', 'N/A')
                timestamp = aqi_data['data']['time'].get('iso', 'N/A')
                pm25_value = aqi_data['data']['iaqi'].get('pm25', {}).get('v', 'N/A')

                # Write data to the CSV
                writer.writerow([now.strftime("%Y-%m-%d %H:%M:%S"), city_name, aqi, dominant_pollutant, pm25_value, timestamp])
    
    print(f"AQI data saved to {filename}")


# Replace with actual city names and token
cities = ["jakarta", "new york", "london", "beijing", "singapore"]

# Fetch and save AQI data
save_aqi_to_csv(cities, api_token)
