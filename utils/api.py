from utils.http_methods import Http_method
import random
from .request_db import db_call

"""Методы для тестирования autoclub"""

class Autoclub_api():
    class Authorization_registration_api():
        """Запрос кода на регистрацию"""
        @staticmethod
        def sign_up(base_url, number="random_number", name_user="autotest"):

            print("\nЗапрос кода на регистрацию")
            if number == "random_number":
                number = "7" + (''.join([random.choice(list('1234567890')) for x in range(10)]))
            else:
                number = number

            json_for_sign_up = {
                    "phone": number,
                    "name": name_user
            }
            print(json_for_sign_up)
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

            json_for_resend_code = {"phone": otp_token}

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
        def email_verify(otp_token, base_url, db_cursor):

            print("\nЗапрос на подтверждение кода авторизации по email")

            resource_email_verify = "/auth/email/verify"
            resource_email_verify_url = base_url + resource_email_verify

            code = db_call.get_code(otp_token, db_cursor)
            json_body_email_verify = {"otp_token":otp_token, "code":code}

            result = Http_method.post(resource_email_verify_url, json_body_email_verify)

            return result

        """(тел)Подтверждение запроса на регистраци/авторизацию/смену номера"""
        @staticmethod
        def phone_verify(otp_token, base_url, db_cursor):

            print("\n(тел)Запрос на подтверждение кода регистраци/авторизацию/смену номера")

            resource_phone_verify = "/auth/phone/verify"
            resource_phone_verify_url = base_url + resource_phone_verify

            code = db_call.get_code(otp_token, db_cursor)
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