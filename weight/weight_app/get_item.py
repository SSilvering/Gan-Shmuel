import mysql.connector

def get_sql(to_time,from_time,id):
    

    data = {
        "id":id,
        "tara":to_time,
        "sessions":from_time
    }
    return data