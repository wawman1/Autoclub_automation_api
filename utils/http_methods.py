from http.cookiejar import Cookie
from wsgiref import headers
import requests

"""Список HTTP методов"""

class Http_method:
    headers = {'Accept': 'application/json'}
    cookie = ""

    @staticmethod
    def get(url):
        result = requests.get(url, headers=Http_method.headers, cookies=Http_method.cookie)
        return result

    @staticmethod
    def post(url, body):
        result = requests.post(url, headers=Http_method.headers, cookies=Http_method.cookie, json=body)
        return result
    
    @staticmethod
    def patch(url, body):
        result = requests.patch(url, headers=Http_method.headers, cookies=Http_method.cookie, json=body)
        return result
    
    @staticmethod
    def delete(url, body):
        result = requests.delete(url, headers=Http_method.headers, cookies=Http_method.cookie, json=body)
        return result