import requests
import datetime as dt
import os



headers = {
    "Content-Type": "application/json",
    "x-app-id": os.environ['Nutrition_API_ID'],
    "x-app-key": os.environ['Nutrition_API_KEY'],

}


answer = input("What excercise did you perform and did you eat anything?")




# NUTRIENTS REQUEST
API = "https://trackapi.nutritionix.com/v2/natural/nutrients"

json_1 = {
    "query": f"{answer}",
    "timezone": "US/Eastern"

}
# response = requests.post(url=API, headers=headers, json=json_1)
# print(response.text)

# EXCERCISE REQUESTS
API_EXCERCISE = "https://trackapi.nutritionix.com/v2/natural/exercise"

json_2 = {
 "query":f"{answer}",
 "gender":"male",
 "weight_kg":53,
 "height_cm":157,
 "age":24
}

response_excercise = requests.post(url=API_EXCERCISE, headers=headers, json=json_2)


# DATETIME

SHEETY_BEARER = {
    "Authorization": f"{os.environ['BEARER_AUTHENTICATION']}"
}

calories_burned = round(response_excercise.json()["exercises"][0]["nf_calories"])
time_spent = response_excercise.json()["exercises"][0]["duration_min"]
time_spent_remaining_sec = round((time_spent*60)%60)
time_spent_remaining = int((round((time_spent*60))-time_spent_remaining_sec)/(60))
excercise = response_excercise.json()["exercises"][0]["user_input"]

converted_time = (f"{time_spent_remaining}:{time_spent_remaining_sec}")


date = dt.datetime.now()
date_year = date.strftime("%Y")
date_month = date.strftime("%m")
date_day = date.strftime("%d")

current_date = f"{date_day}/{date_month}/{date_year}"
current_time = date.strftime("%X")

# print(time_spent_converted)
# SHEETY
SHEETY_API = "https://api.sheety.co/dc1d399fcd2b665f3f8eb739db9d6a20/carbtrial/workouts"

json_3 = {
  "workout": {
      "date": f"{current_date}",
      "time": f"{current_time}",
      "exercise": f"{excercise}",
      "duration": f"{converted_time}",
      "calories": f"{calories_burned}"
  }
}



response_sheety = requests.post(url=f"{SHEETY_API}",json=json_3, headers=SHEETY_BEARER)

