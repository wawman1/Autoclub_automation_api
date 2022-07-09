import requests
import allure
from utils.logger import Logger

"""Список HTTP методов"""

class Http_method:
    headers = {'Accept': 'application/json'}
    cookie = ""

    @staticmethod
    def get(url):
        with allure.step("GET"):
            Logger.add_request(url, method="GET")
            result = requests.get(url, headers=Http_method.headers, cookies=Http_method.cookie)
            Logger.add_response(result)
            return result

    @staticmethod
    def post(url, body):
        with allure.step("POST"):
            Logger.add_request(url, method="POST")
            result = requests.post(url, json=body, headers=Http_method.headers, cookies=Http_method.cookie)
            Logger.add_response(result)
            return result
    
    @staticmethod
    def patch(url, body):
        Logger.add_request(url, method="PATCH")
        result = requests.patch(url, headers=Http_method.headers, cookies=Http_method.cookie, json=body)
        Logger.add_response(result)
        return result
    
    @staticmethod
    def delete(url, body):
        with allure.step("DELETE"):
            Logger.add_request(url, method="DELETE")
            result = requests.delete(url, headers=Http_method.headers, cookies=Http_method.cookie, json=body)
            Logger.add_response(result)
            return result
            
    @staticmethod
    def put(url, body):
        with allure.step("PUT"):
            Logger.add_request(url, method="PUT")
            result = requests.put(url, json=body, headers=Http_method.headers, cookies=Http_method.cookie)
            Logger.add_response(result)
            return result