import pyodbc 
from transform import transform_results
from extract import get_data,city_list
from datetime import datetime


SERVER = "localhost"
DATABASE = "WeatherDataDB"


connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

try :
    conn = pyodbc.connect(connection_string)
    if conn:
        print("connected successfuly")
    conn.close()
    
except pyodbc.Error as e :
    print(f"failed to connect to DB :{e}")


def run_query(query:str)->list:
    conn=pyodbc.connect(connection_string)
    csr=conn.cursor()
    csr.execute(query)
    query_result=csr.fetchall()
    csr.close()
    conn.close()

    return query_result

def insert_data(query:str,data:list)-> int:
    conn=pyodbc.connect(connection_string)
    csr=conn.cursor()
    csr.fast_executemany=True
    csr.executemany(query,data)
    conn.commit()
    rows_inserted = csr.rowcount
    csr.close()
    conn.close()

    return rows_inserted


query= """
INSERT INTO WeatherData 
([country_name],[country_code],[timestamp],[temperature],[feels_like],[humidity],[wind_speed],[weather_description])
VALUES (?,?,?,?,?,?,?,?)
"""


raw_data=get_data(city_list["cities"])

clean_data=transform_results(raw_data)
data_tuple=[]

for d in clean_data:
    row=(
        d['country_name'],
        d['country_code'],
        datetime.fromtimestamp(d['timestamp']),
        d['temperature'],
        d['feels_like'],
        d['humidity'],
        d['wind_speed'],
        d['weather_description']
    )
    data_tuple.append(row)

insert_data(query,data_tuple)