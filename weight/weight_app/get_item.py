import mysql.connector


def get_sql(to_time,from_time,id,query):
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

    fetcher.execute(query) #run sql query

    for lines in fetcher: #iterate through our returned object (data,data,data,data)
        print(x)

    data = {
        "id":id,
        "tara":to_time,
        "sessions":from_time
    }

    #close connections
    fetcher.close()
    database.close()

    return data