import pyodbc 


SERVER: str = "localhost"
DATABASE: str = "WeatherDataDB"


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
    conn=pyodbc.connect(connection_string)
    csr=conn.cursor()
    csr.fast_executemany=True
    csr.executemany(query,data)
    conn.commit()
    rows_inserted = len(data)
    csr.close()
    conn.close()

    return rows_inserted

# def truncate_table (query:str):
#     conn=pyodbc.connect(connection_string)
#     csr=conn.cursor()
#     csr.execute(query)
#     conn.commit()
#     csr.close()
#     conn.close()
