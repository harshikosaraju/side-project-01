import os
from dotenv import load_dotenv
import base64
import requests
import time

# Load environment variables from .env file
load_dotenv()

# Get secrets from environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Base URL for the API
BASE_URL = "https://api.kroger.com/v1"

# Global variable to store token and expiration time
access_token = None
token_expires_at = 0

def get_access_token():
    """
    Fetch a new access token using client credentials.
    """
    global access_token, token_expires_at

    # Encode the credentials
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    base64_auth = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")

    # Make the request
    url = f"{BASE_URL}/connect/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {base64_auth}",
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raise exception for bad responses

    # Parse and store the token
    token_data = response.json()
    access_token = token_data["access_token"]
    token_expires_at = time.time() + token_data["expires_in"]  # Current time + token lifespan

    print("New access token retrieved!")
    return access_token

def ensure_valid_token():
    """
    Ensure the token is valid, refreshing it if necessary.
    """
    global access_token, token_expires_at
    if access_token is None or time.time() >= token_expires_at:
        get_access_token()

def search_products(term, location_id):
    """
    Search for products using the Kroger API.
    """
    ensure_valid_token()

    url = f"{BASE_URL}/products?filter.term={term}&filter.locationId={location_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise exception for bad responses

    return response.json()

def fetch_product_details(product_id):
    """
    Fetch details for a specific product by ID.
    """
    ensure_valid_token()

    url = f"{BASE_URL}/products/{product_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise exception for bad responses

    return response.json()

if __name__ == "__main__":
    # Example: Search for apples at a specific location
    location_id = "01400943"  # Replace with a valid location ID
    products = search_products("apples", location_id)
    print("Search Results:", products)

    # Example: Fetch details for the first product
    if "data" in products and len(products["data"]) > 0:
        product_id = products["data"][0]["productId"]
        product_details = fetch_product_details(product_id)
        print("Product Details:", product_details)
