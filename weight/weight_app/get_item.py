import mysql.connector


def get_sql(to_time,from_time,id):
    try:
        database = mysql.connector.connect(
            host='db',
            user='root',
            password='123',
            database="weight_testing_db"
        )
    except:
        return "Database connection refused..."

    fetcher = database.cursor()

    query = f"SELECT (bruto,neto,id) FROM sessions"

    fetcher.execute(query) #run sql query


    for line in 
    data = {
        "id":id,
        "tara":0,
        "sessions":[]
    }

    # for (bruto,neto,id) in fetcher: #iterate through our returned object (data,data,data,data)
    #     data["tara"] = float(bruto) - float(neto)
    #     data["sessions"].append(id)


    #close connections
    fetcher.close()
    database.close()

    return data