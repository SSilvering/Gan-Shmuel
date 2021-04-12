from weight_app import weight_app
import mysql.connector


class DB_Module(object):
    def __init__(self):
        self.db_user = "root"
        self.db_pass = "123"
        self.db_host = "db"
        self.db_name = "weight_testing_db"
        self.sqlp = f"user='{self.db_user}', password='{self.db_pass}', host='{self.db_host}', database='{self.db_name}'"
        self.open_connection = None
    
    def getConnection(self):
        #sqlp = f"user='{self.db_user}', password='{self.db_pass}', host='{self.db_host}', database='{self.db_name}'"
        #sqlp = f"user='root', password='123', host='db', database='weight_testing_db'"
        if self.open_connection is None:
            self.open_connection = mysql.connector.connect(user='root', password='123', host='db', database='weight_testing_db')

        return self.open_connection

    def fetch_new_data(self,SELECT_QUERY):
        rows_list = []

        conn = self.getConnection()
        cur = conn.cursor(dictionary=True, buffered=True)
        #curs = conn.cursor(cur)
        #cur = conn.cursor()
        res = cur.execute(SELECT_QUERY)
        
        for result_row in cur:
            rows_list.append(result_row)
        
        #row_list is a list containing tuples

        return rows_list

    def insert_new_data(self,query,values):
        conn = self.getConnection()
        cur = conn.cursor()

        for index in range(0,len(values)):
            cur.execute(query,values[index])
        conn.commit()

