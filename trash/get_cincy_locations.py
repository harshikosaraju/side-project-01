import os
from dotenv import load_dotenv
import base64
import requests
import time

# Load environment variables from .env file
load_dotenv()

# Get secrets from environment variables
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# Define the headers for authorization
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# Define the API URL with zip code and radius
api_url = "https://api.kroger.com/v1/locations"
params = {
    "filter.zipCode": "45219",  # Cincinnati, OH area zip code
    "filter.radiusInMiles": "100"  # Specify the radius in miles
}

# Make the GET request
response = requests.get(api_url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    print("Nearby Kroger Locations:", data)
else:
    print(f"Error fetching locations: {response.status_code}")