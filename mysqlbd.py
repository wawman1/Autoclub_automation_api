import mysql.connector
from mysql.connector import Error
from config import db_config 

def create_connection_mysql_db(db_host, user_name, user_password, db_name = None):
    connection_db = None
    try:
        connection_db = mysql.connector.connect(
            host = db_host,
            user = user_name,
            passwd = user_password,
            database = db_name
        )
        print("Подключение к MySQL успешно выполнено")
    except Error as db_connection_error:
        print("Возникла ошибка: ", db_connection_error)
    return connection_db

conn = create_connection_mysql_db(db_config["mysql"]["host"], 
                                  db_config["mysql"]["user"], 
                                  db_config["mysql"]["pass"],
                                  db_config["mysql"]["database"])
cursor = conn.cursor()
try:
    # изблечение данных из бд
    select_users_female_query = '''
    SELECT * FROM users limit 5;
    '''
    cursor.execute(select_users_female_query)
    query_result = cursor.fetchall()
    for user in query_result:
        print(user)

except Error as error:
    print(error)
finally:
    cursor.close()
    conn.close()                                 