def transform_results(results:list)->list:
    cleaned_city=[]
    for city in results:
        city_info={
            "city_name":city.get('name'),
            "country_code":city['sys'].get('country'),
            "timestamp":city.get('dt'),
            "temperature":city['main'].get('temp'),
            "feels_like":city['main'].get('feels_like',0),
            "humidity":city['main'].get('humidity'),
            "wind_speed":city['wind'].get('speed',0),
            "weather_description":city.get('weather',[{}])[0].get('description','Unknown')
        }
        cleaned_city.append(city_info)
    return cleaned_city
        
