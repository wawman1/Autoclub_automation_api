import requests
from unittest import result
from utils.http_methods import Http_method
import random

"""Методы для тестирования autoclub"""

base_url = "http://autoclub-back.eclipseds.ru/api/v1"
bearer_token = ""           #тут будет переменная из запросов авторизации

class Autoclub_api():

    """Запрос на регистрацию"""
    @staticmethod
    def sign_up():

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
        return result
        
    """(тел)Подтверждение запроса на регистраци/авторизацию/смену номера"""
    @staticmethod
    def phone_verify(json_sms):

        print("Запрос на подтверждение кода регистрации")

        post_resource_phone_verify = "/auth/phone/verify"
        post_resource_phone_verify_url = base_url + post_resource_phone_verify
        print(post_resource_phone_verify_url)
        result = Http_method.post(post_resource_phone_verify_url, json_sms)
        # auth_token = result.json().get("auth_token")
        result.encoding = "utf-8"
        reaspons = result.json()
        phone_verify_status_code = "статус код = " + str(result.status_code)
        print(phone_verify_status_code, reaspons)
        return result