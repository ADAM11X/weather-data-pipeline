import pyodbc 
import logging

SERVER: str = "localhost"
DATABASE: str = "WeatherDataDB"

logging.basicConfig(level=logging.INFO ,
                    filename="logs/pipeline.log" ,
                    filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

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

def insert_data(query:str,data=None)-> int:
    try : 
        conn=pyodbc.connect(connection_string)
        csr=conn.cursor()
        csr.fast_executemany=True
        csr.executemany(query,data)
        conn.commit()
        rows_inserted = len(data)
        logging.info(f"Data was inserted successfully")
        return rows_inserted
    except pyodbc.Error as e :
        if conn:
            conn.rollback()
        logging.error(f"failed to insert data into DB , rolled back :{e}")
        return 0
    finally: 
        if csr:
            csr.close()
        if conn:
            conn.close()
