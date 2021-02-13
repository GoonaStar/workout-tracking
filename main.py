import requests
from datetime import datetime
import os

APP_ID = os.getenv("APP_ID_X")
API_KEY = os.getenv("API_KEY_X")

BASIC_AUTH = (os.getenv("USERNAME"), os.getenv("PASSWORD"))

GENDER = "male"
WEIGHT_KG = 78
HEIGHT_CM = 184
AGE = 24

origin_endpoint = "https://trackapi.nutritionix.com/"
natural_exercise_endpoint = "/v2/natural/exercise"

today = datetime.now()
today_date = today.strftime("%H/%M/%S")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "x-remote-user-id": "0",
}

exercise_params = {
    "query": input("Tell me which exercises you did:\n"),
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=f"{origin_endpoint}{natural_exercise_endpoint}",
                         json=exercise_params,
                         headers=headers,
                         auth=BASIC_AUTH)
results = response.json()

for result in results["exercises"]:
    workouts_params = {
        "workout": {
            "date": today.strftime("%Y/%m/%d"),
            "time": today.strftime("%X"),
            "exercise": results["exercises"][0]["name"].title(),
            "duration": results["exercises"][0]["duration_min"],
            "calories": results["exercises"][0]["nf_calories"],
        }
    }

sheety_endpoint = os.getenv("SHEET_ENDPOINT")
add_row = requests.post(url=sheety_endpoint, json=workouts_params, auth=BASIC_AUTH)
print(add_row.text)
