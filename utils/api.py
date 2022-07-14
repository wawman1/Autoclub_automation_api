from utils.http_methods import Http_method
import random
from .request_db import db_call

"""Методы для тестирования autoclub"""

class Autoclub_api():

    """Запрос на регистрацию"""
    @staticmethod
    def sign_up(base_url):

        print("Запрос кода на регистрацию")

        random_number = ''.join([random.choice(list('1234567890')) for x in range(10)])
        json_for_sign_up = {
            "phone": "7" + random_number,
            "name": "autotest"
        }

        post_resource_sign_up = "/auth/phone/sign-up"
        post_resource_sign_up_url = base_url + post_resource_sign_up
        print(post_resource_sign_up_url)

        result = Http_method.post(post_resource_sign_up_url, json_for_sign_up)
        result.encoding = "utf-8"
        reaspons = result.json()
        sign_up_status_code = "статус код = " + str(result.status_code)
        print(sign_up_status_code, reaspons)

        # otp_token = result.json().get("otp_token")
        return result
        
    """(тел)Подтверждение запроса на регистраци/авторизацию/смену номера"""
    @staticmethod
    def phone_verify(otp_token, base_url, db_cursor):

        print("Запрос на подтверждение кода регистрации")

        post_resource_phone_verify = "/auth/phone/verify"
        post_resource_phone_verify_url = base_url + post_resource_phone_verify
        print(post_resource_phone_verify_url)

        code = db_call.get_code(otp_token, db_cursor)
        json_body_bophone_verify = {"otp_token":otp_token, "code":code}

        result = Http_method.post(post_resource_phone_verify_url, json_body_bophone_verify)
        result.encoding = "utf-8"
        reaspons = result.json()
        phone_verify_status_code = "статус код = " + str(result.status_code)
        print(phone_verify_status_code, reaspons)
        return result

    @staticmethod
    def profile(base_url, auth_token):
        profile_resource = '/user/profile'
        get_resource_profile_url = base_url + profile_resource
        print(get_resource_profile_url)
        result = Http_method.get(get_resource_profile_url, auth_token)
        result.encoding = "utf-8"
        reaspons = result.json()
        get_resource_profile_status_code = "статус код = " + str(result.status_code)
        print(get_resource_profile_status_code, reaspons)
        return result