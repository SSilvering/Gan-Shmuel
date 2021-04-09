import mysql.connector

sql_config= {
    "host":'db',
    "user":'root',
    "password":'123',
    "database":"weight_testing_db"
}

def get_sql(to_time,from_time,id):
    

    data = {
        "id":id,
        "tara":to_time,
        "sessions":from_time
    }
    return data