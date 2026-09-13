
from src.extract import get_data, city_list
from src.transform import transform_results
from src.load import insert_data
from datetime import datetime


print("Extracting data from OpenWeather API...")
raw_data = get_data(city_list['cities'])
print(f"Extracted data for {len(raw_data)} cities")



print("Transforming data...")
clean_data = transform_results(raw_data)
print(f"Transformed {len(clean_data)} records")



print("Loading data into SQL Server...")


query= """
INSERT INTO WeatherData 
([city_name],[country_code],[timestamp],[temperature],[feels_like],[humidity],[wind_speed],[weather_description])
VALUES (?,?,?,?,?,?,?,?)
"""



data_tuple=[]

for d in clean_data:
    row=(
        d['city_name'],
        d['country_code'],
        datetime.fromtimestamp(d['timestamp']),
        d['temperature'],
        d['feels_like'],
        d['humidity'],
        d['wind_speed'],
        d['weather_description']
    )
    data_tuple.append(row)


rows_inserted=insert_data(query,data_tuple)

print(f"Rows inserted: {rows_inserted}")
