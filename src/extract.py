import requests 
import os
from dotenv import load_dotenv
import json 


load_dotenv()


API_KEY = os.getenv("OPENWEATHER_API_KEY")


if not API_KEY : 
    raise ValueError("API key not found. Check your .env file.")


try:
    with open("config/cities.json","r") as f:
        city_list=json.load(f)
        

except FileNotFoundError: 
    raise FileNotFoundError("config/cities.json not found")

except ValueError : 
    raise ValueError ("cities.json is not valid JSON")


def get_data(cities)->list:
    results=[]
    for city in cities :
        print(city)
        try :
            data=api_call(city,API_KEY)
            if data :
                results.append(data)
            
        except requests.exceptions.RequestException as e:
            print(f"Network error for {city}: {e}")
            continue
    return results




def api_call(City:str,Api_key:str)->dict|None:

    BASE_URL= f"https://api.openweathermap.org/data/2.5/weather?q={City}&appid={Api_key}&units=metric"
    try :
        response=requests.get(BASE_URL,timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    
    if response.status_code == 200 : 
        DATA=response.json()
        return DATA
    elif response.status_code == 404:
        print(f"City Not Found : {City}")
        return None
    elif response.status_code == 401:
        print("Invalid API key , check OPENWEATHER_API_KEY in .env file ")
        exit(1)
    elif response.status_code == 429:
        print("Rate limit hit	Wait a few seconds, retry")
        return None
    else:
        print(f"Unexpected error for {City}: {response.status_code}")
        return None

data = get_data(city_list['cities'])

print(type(data))