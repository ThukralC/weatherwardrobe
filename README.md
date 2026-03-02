# WeatherWardrobe (Milestone #2) - Database Connection Demo

This folder contains a minimal Python script to demonstrate cloud database access for **Milestone #2**.

## What it does
- Connects to **Firebase Firestore**
- Adds a sample document into the `wardrobe_items` collection
- Reads back and prints the first 10 items

## Setup
1. Create a Firebase project: https://console.firebase.google.com
2. Enable **Firestore Database**
3. Create and download a **Service Account key** (JSON)
4. Place the file in this folder as: `serviceAccountKey.json`

> IMPORTANT: Do NOT commit `serviceAccountKey.json` to a public GitHub repository.

## Install
```bash
pip install firebase-admin
```

## Run
```bash
python main.py
```
