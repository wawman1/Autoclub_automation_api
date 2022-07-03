from requests import Response

"""Библеотека проверок ответов"""
class Cheking():

    @staticmethod
    def check_status_code(respons: Response, status_code):
        assert status_code == respons.status_code, "не верный статус код, ожидаемый код = " + str(status_code) + " полученный код = " + str(respons.status_code)
        
