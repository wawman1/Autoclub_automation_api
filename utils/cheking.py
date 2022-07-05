"""Библеотека проверок ответов"""
class Cheking():

    """Метод для проверки статус кодов"""
    @staticmethod
    def check_status_code(respons, status_code):
        assert status_code == respons.status_code, "не верный статус код, ожидаемый код = " + str(status_code) + " полученный код = " + str(respons.status_code)
        print("проверка статус кода успешна" )
    
    """Метод для проверки ключей ответа"""
    @staticmethod
    def check_json_property(respons, expected_value):
        json_respons = respons.json() 
        print("проверка ключей ответа успешна")
        assert expected_value == list(json_respons), "не верные ключи ответа, ожидались = " + str(expected_value) + " были получены = " + str(list(json_respons))