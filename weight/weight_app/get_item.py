import mysql.connector

def get_sql(to_time,from_time,id):


    data = {
        "id":id,
        "tara":1,
        "sessions":[1,2,3]
    }
    return data