from mysql.connector import Error

class db_call():
    def get_code(otp_token, db_cursor):
        try:
            select_users_female_query = "SELECT code FROM `verify_codes` where verify_request_id = (SELECT id FROM `verify_requests` where otp_token = '"  + str(otp_token) + "')"
            db_cursor.execute(select_users_female_query)
            query_result = db_cursor.fetchone()

        except Error as error:
            print(error)
        return query_result[0]