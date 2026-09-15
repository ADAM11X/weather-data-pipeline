from src.extract import get_data, city_list
from src.transform import transform_results
from src.load import insert_data
from datetime import datetime
import logging 


logging.basicConfig(level=logging.INFO ,
                    filename="logs/pipeline.log" ,
                    filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")


logging.info("Extracting data from OpenWeather API...")
raw_data = get_data(city_list['cities'])
logging.info(f"Extracted data for {len(raw_data)} cities")


logging.info("Transforming data...")
clean_data = transform_results(raw_data)
logging.info(f"Transformed {len(clean_data)} records")


logging.info("Loading data into SQL Server...")


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

logging.info(f"Rows inserted: {rows_inserted}")
