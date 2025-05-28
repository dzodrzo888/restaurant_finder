from dotenv import load_dotenv
import os
from pathlib import Path
import time
import googlemaps


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=BASE_DIR / '.env')
api_key = os.getenv("key")

gmaps = googlemaps.Client(key=api_key)

location_PRG = (50.073658, 14.418540)

def get_nearby_restaurants(location: tuple, radius=1000, keyword=None, page_token=None) -> tuple:
    """
    Get nearby restaurants based on location and optional keyword.
    
    Args:
        location (tuple): Tuple of latitude and longitude (lat, lng).
        radius (int): Search radius in meters.
        keyword (str): Optional keyword to filter results.
        page_token (str): Token for fetching the next page of results.
    Returns: 
        (tuple): Tuple containing list of nearby restaurants and next page token.
    """
    if page_token:
        print(page_token)
        places = gmaps.places_nearby(location=location, radius=radius, keyword=keyword, type='restaurant', page_token=page_token)
    else:
        places = gmaps.places_nearby(location=location, radius=radius, keyword=keyword, type='restaurant')
    results = places.get('results', [])
    next_page_token = places.get("next_page_token")
    return results, next_page_token

def get_all_restaurants(num_pages=None):
    all_results = []
    page_index = 0
    page_token = None

    while True:
        time.sleep(0.01)
        results, page_token = get_nearby_restaurants(location=location_PRG, radius=1000, page_token=page_token)
        all_results.extend(results)
        page_index += 1
        if num_pages and page_index >= num_pages:
            break
        if not page_token:
            break
    
    return all_results

all_results = get_all_restaurants(num_pages=10)

print(all_results)