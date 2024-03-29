from utils.http_methods import Http_method
from conftest import Secondary_functions
from .request_db import db_call

"""Методы для тестирования autoclub"""

class Autoclub_api():
    class Authorization_registration_api():
        """Запрос кода на регистрацию"""
        @staticmethod
        def sign_up(base_url, phone="random_phone", name_user="autotest"):

            print("\nЗапрос кода на регистрацию")
            if phone == "random_phone":
                phone = Secondary_functions.random_phone()

            json_for_sign_up = {
                    "phone": phone,
                    "name": name_user
            }
            
            resource_sign_up = "/auth/phone/sign-up"
            resource_sign_up_url = base_url + resource_sign_up

            result = Http_method.post(resource_sign_up_url, json_for_sign_up)

            return result

        """Запрос кода на авторизацию по номеру"""
        @staticmethod
        def sign_in(base_url, phone):

            print("\nЗапрос кода на авторизацию по номеру")

            resource_sign_in = "/auth/phone/sign-in"
            resource_sign_in_url = base_url + resource_sign_in

            json_for_sign_in = {"phone": phone}

            result = Http_method.post(resource_sign_in_url, json_for_sign_in)

            return result

        """Запрос на повторную отправку кода"""
        @staticmethod
        def resend_code(base_url, otp_token):

            print("\nЗапрос на повторную отправку кода")

            resource_resend_code = "/auth/code/resend"
            resource_resend_code_url = base_url + resource_resend_code

            json_for_resend_code = {"otp_token": otp_token}

            result = Http_method.post(resource_resend_code_url, json_for_resend_code)

            return result

        """Запрос кода на авторизацию по email"""
        @staticmethod
        def email_sign_in(base_url, email):

            print("\nЗапрос кода на авторизацию по email")

            resource_email_sign_in = "/auth/email/sign-in"
            resource_email_sign_in_url = base_url + resource_email_sign_in

            json_for_email_sign_in = {"email": email}

            result = Http_method.post(resource_email_sign_in_url, json_for_email_sign_in)

            return result
            
        """Запрос на подтверждение кода авторизации по email"""
        @staticmethod
        def email_verify(base_url, otp_token, db_cursor):

            print("\nЗапрос на подтверждение кода авторизации по email")

            if str(type(db_cursor)) == "<class 'mysql.connector.cursor_cext.CMySQLCursor'>": # пока ничего лучше не придумал для реализации негативных кейсов с кодом
                code = db_call.get_code(otp_token, db_cursor)
            else:
                code = db_cursor

            resource_email_verify = "/auth/email/verify"
            resource_email_verify_url = base_url + resource_email_verify

            json_body_email_verify = {"otp_token":otp_token, "code":code}

            result = Http_method.post(resource_email_verify_url, json_body_email_verify)

            return result

        """(тел)Подтверждение запроса на регистраци/авторизацию/смену номера"""
        @staticmethod
        def phone_verify(base_url, otp_token, db_cursor):

            print("\n(тел)Запрос на подтверждение кода регистраци/авторизацию/смену номера")

            if str(type(db_cursor)) == "<class 'mysql.connector.cursor_cext.CMySQLCursor'>": # пока ничего лучше не придумал для реализации негативных кейсов с кодом
                code = db_call.get_code(otp_token, db_cursor)
            else:
                code = db_cursor

            resource_phone_verify = "/auth/phone/verify"
            resource_phone_verify_url = base_url + resource_phone_verify

            json_body_bophone_verify = {"otp_token":otp_token, "code":code}

            result = Http_method.post(resource_phone_verify_url, json_body_bophone_verify)

            return result

        """Запрос выхода из профиля"""
        @staticmethod
        def logout(base_url, auth_token):

            print("\nЗапрос выхода из профиля")

            resource_logout = "/auth/logout"
            resource_logout_url = base_url + resource_logout

            result = Http_method.post(url = resource_logout_url, auth_token = auth_token)

            return result

    class Profile_api():
        """Запрос на получение данных профиля"""
        @staticmethod
        def profile(base_url, auth_token):

            print("\nЗапрос на получение данных профиля")

            profile_resource = '/user/profile'
            resource_profile_url = base_url + profile_resource

            result = Http_method.get(resource_profile_url, auth_token)

            return result
        
        """Запрос изменение данных профиля"""
        @staticmethod
        def profile_update(base_url, auth_token, name=None, email=None, birth_date=None):

            print("\nЗапрос изменение данных профиля")

            profile_resource = '/user/profile/update'
            resource_profile_url = base_url + profile_resource

            json_for_profile_update = {}

            if name!= None:
                json_for_profile_update["name"] = name

            if email!= None:
                json_for_profile_update["email"] = email

            if birth_date!= None:
                json_for_profile_update["birth_date"] = birth_date


            result = Http_method.patch(resource_profile_url, body=json_for_profile_update, auth_token=auth_token)

            return result