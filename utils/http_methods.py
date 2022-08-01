import requests
import allure
from utils.logger import Logger

"""Список HTTP методов"""

class Http_method:

    """Создание словаря headers для передачи их в запросы"""
    def headers(auth_token):
        headers_value = {'Accept': 'application/json'}
        if auth_token != None:                              #если запрос отмечен как авторизованный, то передает в него токен авторизации
            headers_value['Authorization'] = auth_token
        return headers_value
    cookie = ""

    @staticmethod
    def get(url, auth_token=None):
        with allure.step("GET " + url):
            Logger.add_request(url, method="GET")
            print("GET " + url)
            result = requests.get(url, headers=Http_method.headers(auth_token), cookies=Http_method.cookie)
            Logger.add_response(result)
            result.encoding = "utf-8"
            reaspons = result.json()
            print("статус код = " + str(result.status_code), reaspons)
            return result

    @staticmethod
    def post(url, body=None, auth_token=None):
        with allure.step("POST " + url):
            Logger.add_request(url, method="POST")
            print("POST " + url)
            result = requests.post(url, headers=Http_method.headers(auth_token), cookies=Http_method.cookie, json=body)
            Logger.add_response(result)
            result.encoding = "utf-8"
            reaspons = result.json()
            print("статус код = " + str(result.status_code), reaspons)
            return result
    
    @staticmethod
    def patch(url, body=None, auth_token=None):
        with allure.step("POST " + url):
            Logger.add_request(url, method="PATCH")
            print("PATCH " + url)
            result = requests.patch(url, headers=Http_method.headers(auth_token), cookies=Http_method.cookie, json=body)
            Logger.add_response(result)
            result.encoding = "utf-8"
            reaspons = result.json()
            print("статус код = " + str(result.status_code), reaspons)
            return result
    
    @staticmethod
    def delete(url, body=None, auth_token=None):
        with allure.step("DELETE " + url):
            Logger.add_request(url, method="DELETE")
            print("DELETE " + url)
            result = requests.delete(url, headers=Http_method.headers(auth_token), cookies=Http_method.cookie, json=body)
            Logger.add_response(result)
            result.encoding = "utf-8"
            reaspons = result.json()
            print("статус код = " + str(result.status_code), reaspons)
            return result
            
    @staticmethod
    def put(url, body=None, auth_token=None):
        with allure.step("PUT " + url):
            Logger.add_request(url, method="PUT")
            print("PUT " + url)
            result = requests.put(url,headers=Http_method.headers(auth_token), cookies=Http_method.cookie, json=body)
            Logger.add_response(result)
            result.encoding = "utf-8"
            reaspons = result.json()
            print("статус код = " + str(result.status_code), reaspons)
            return result