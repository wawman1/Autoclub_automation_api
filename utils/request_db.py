from mysql.connector import Error

"""Библиотека скриптов для обращения к базе данных"""
class db_call():

    """Получение кода по otp_token"""
    def get_code(otp_token, db_cursor):
        try:
            select_users_female_query = "SELECT code FROM `verify_codes` where verify_request_id = (SELECT id FROM `verify_requests` where otp_token = '"  + str(otp_token) + "')"
            db_cursor.execute(select_users_female_query)
            query_result = db_cursor.fetchone()

        except Error as error:
            print(error)
        return query_result[0]
    
    """Проверка отсутствия пользователя с указанным телефоном"""
    def check_user_phone(phone, db_cursor):
        try:
            select_users_female_query = "SELECT count(*) FROM `users` where phone = "  + str(phone)
            db_cursor.execute(select_users_female_query)
            query_result = db_cursor.fetchone()

        except Error as error:
            print(error)
        return query_result[0]
    
