# filters and recommends clothing items based on current weather
# uses Specification pattern for filtering
# uses Strategy pattern for scoring items


from factory import ClothingFactory
from strategy import RecommendationStrategy
from specification import TempSpec
from datetime import datetime
import os
import firebase_admin
from firebase_admin import credentials, firestore


def init_firestore():
    key_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")

    if not firebase_admin._apps:
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)

    return firestore.client()


def add_sample_items(db):
    items = [
        {
            "name": "Rain Jacket",
            "category": "outerwear",
            "temp_min_c": -5,
            "temp_max_c": 12,
            "waterproof": True,
            "wind_protection": "medium",
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "name": "Hoodie",
            "category": "top",
            "temp_min_c": 5,
            "temp_max_c": 18,
            "waterproof": False,
            "wind_protection": "low",
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "name": "Winter Coat",
            "category": "outerwear",
            "temp_min_c": -25,
            "temp_max_c": 5,
            "waterproof": False,
            "wind_protection": "high",
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "name": "Sneakers",
            "category": "footwear",
            "temp_min_c": 0,
            "temp_max_c": 30,
            "waterproof": False,
            "wind_protection": "low",
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "name": "Umbrella",
            "category": "accessory",
            "temp_min_c": -10,
            "temp_max_c": 35,
            "waterproof": True,
            "wind_protection": "low",
            "created_at": datetime.utcnow().isoformat()
        }
    ]

    ids = []

    for item in items:
        doc_ref = db.collection("wardrobe_items").document()
        doc_ref.set(item)
        ids.append(doc_ref.id)

    return ids


def read_items(db):
    docs = db.collection("wardrobe_items").limit(10).stream()

    print("\nWardrobe Items:")
    for d in docs:
        data = d.to_dict()
        print(
            d.id,
            "|",
            data.get("name"),
            "|",
            data.get("category"),
            "| waterproof:",
            data.get("waterproof")
        )
import requests

def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(url, params=params)
    data = response.json()

    #  HANDLE ERROR
    if response.status_code != 200:
        print("\nError fetching weather:", data.get("message"))
        return None

    return {
        "temp": data["main"]["temp"],
        "condition": data["weather"][0]["main"],
        "wind": data["wind"]["speed"]
    }


def recommend_items(db, weather):
    # create pattern objects
    docs = db.collection("wardrobe_items").stream()

    # create pattern objects
    spec = TempSpec()
    strategy = RecommendationStrategy()
    factory = ClothingFactory()

    print("\nRecommended Items:")

    for d in docs:
        item = d.to_dict()
        item = factory.create(item)

        if spec.is_satisfied(item, weather):
            score = strategy.score(item, weather)
            print(item["name"], "|", item["category"], "| score:", score)
            
            
# main function that runs the application flow
# connects database, gets user input, fetches weather, and shows recommendations
# this structure improves maintainability by separating database,
# API, and recommendation logic into different functions
def main():
    db = init_firestore()

# add_sample_items(db)
    read_items(db)
    
# ask user to enter city name
    city = input("\nEnter city: ")

# fetch weather from API
    weather = get_weather(city)
    
    # if API failed, stop execution
    if weather is None:
        print("Try another city or check your API key.")
        return
    
    
    # display weather information
    print("\nWeather:")
    print("Temp:", weather["temp"])
    print("Condition:", weather["condition"])
    print("Wind:", weather["wind"])

# generate outfit recommendations based on weather

    recommend_items(db, weather)

if __name__ == "__main__":
    main()