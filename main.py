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


def main():
    db = init_firestore()

    new_ids = add_sample_items(db)

    print("Added items:")
    for i in new_ids:
        print("-", i)

    read_items(db)


if __name__ == "__main__":
    main()