import requests
import allure
from utils.logger import Logger

"""Список HTTP методов"""

class Http_method:
    def headers(auth_token):
        headers_value = {'Accept': 'application/json'}
        if auth_token != None:
            headers_value['Authorization'] = auth_token
        return headers_value
    cookie = ""

    @staticmethod
    def get(url, auth_token=None):
        with allure.step("GET"):
            Logger.add_request(url, method="GET")
            result = requests.get(url, headers=Http_method.headers(auth_token), cookies=Http_method.cookie)
            Logger.add_response(result)
            return result

    @staticmethod
    def post(url, body, auth_token=None):
        with allure.step("POST"):
            Logger.add_request(url, method="POST")
            result = requests.post(url, headers=Http_method.headers(auth_token), cookies=Http_method.cookie, json=body)
            Logger.add_response(result)
            return result
    
    @staticmethod
    def patch(url, body, auth_token=None):
        Logger.add_request(url, method="PATCH")
        result = requests.patch(url, headers=Http_method.headers(auth_token), cookies=Http_method.cookie, json=body)
        Logger.add_response(result)
        return result
    
    @staticmethod
    def delete(url, body, auth_token=None):
        with allure.step("DELETE"):
            Logger.add_request(url, method="DELETE")
            result = requests.delete(url, headers=Http_method.headers(auth_token), cookies=Http_method.cookie, json=body)
            Logger.add_response(result)
            return result
            
    @staticmethod
    def put(url, body, auth_token=None):
        with allure.step("PUT"):
            Logger.add_request(url, method="PUT")
            result = requests.put(url,headers=Http_method.headers(auth_token), cookies=Http_method.cookie, json=body)
            Logger.add_response(result)
            return result