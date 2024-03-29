import pytest
import random
from utils.http_methods import Http_method
import mysql.connector
from mysql.connector import Error
from config import db_config 
from utils.request_db import db_call

"""Получение указателя сервера при запуске тестов"""
def pytest_addoption(parser):
    parser.addoption('--server', action='store', default="dev",
                     help="Выберите сервер на котором нужно запускать тесты\n доступные варианты: dev")

"""Выдача базовой ссылки по указанному серверу"""
@pytest.fixture(scope="session")    
def base_url(request):
    server_name = request.config.getoption('server')
    if server_name == "dev":
        print("\n\nСтарт тестирования на сервере dev..\n\n")
        base_url = 'http://autoclub-back.eclipseds.ru/api/v1'
        
    # elif server_name == "stage":
    #     print("\nstart server stage for test..")
    #     base_url = ''
    
    # elif server_name == "prod":
    #     print("\nstart server prod for test..")
    #     base_url = ''
        
    else:
        raise pytest.UsageError("не верное имя сервера, доступные варианты: dev")
    return base_url

"""Генерация уникального номера для тестового аккаунта"""
@pytest.fixture(scope="session")    
def phone_user():
    phone_user_test = Secondary_functions.random_phone() 
    print("Сгенерирован уникальный номер для тестового аккаунта")

    return phone_user_test

"""Регистрация нового пользователя и выдача его токена, один тестовый пользователь на сессию"""
@pytest.fixture(scope="session", autouse=True)    
def auth_token(base_url, phone_user):
    print("\n\nПодготовка тестового аккаунта")
    json_for_sign_up = {
        "phone": phone_user,
        "name": "autotest"
    }

    post_resource_sign_up = "/auth/phone/sign-up"
    post_resource_sign_up_url = base_url + post_resource_sign_up
    
    result_sign_up = Http_method.post(post_resource_sign_up_url, json_for_sign_up)
    reaspons_sign_up = result_sign_up.json()

    post_resource_phone_verify = "/auth/phone/verify"
    post_resource_phone_verify_url = base_url + post_resource_phone_verify

    result_phone_verify = Http_method.post(post_resource_phone_verify_url, reaspons_sign_up)
    auth_token = 'Bearer ' + result_phone_verify.json().get("auth_token")
    print("Подготовка тестового аккаунта завершена\n\n")
    return auth_token

"""Выполняет подключение к БД при запуске тестов и закрывает подключение по их завершению"""
@pytest.fixture(scope="function") 
def db_cursor():
    conn = Secondary_functions.create_connection_mysql_db(db_config["mysql"]["host"], 
                                    db_config["mysql"]["user"], 
                                    db_config["mysql"]["pass"],
                                    db_config["mysql"]["database"])
    cursor = conn.cursor()
    yield cursor
    cursor.close()
    conn.close()  
    print("\n\nПодключение к MySQL завершено\n")

class Secondary_functions():

    """Создание подключения к БД"""
    def create_connection_mysql_db(db_host, user_name, user_password, db_name = None):
            connection_db = None
            try:
                connection_db = mysql.connector.connect(
                    host = db_host,
                    user = user_name,
                    passwd = user_password,
                    database = db_name
                )
                print("\nПодключение к MySQL успешно выполнено\n")
            except Error as db_connection_error:
                print("Возникла ошибка: ", db_connection_error)
            return connection_db

    """Генерация уникального номера телефона"""
    def random_phone():
        def random_number():
            random_phone ="7" + ''.join([random.choice(list('1234567890')) for x in range(10)])
            return random_phone
        
        conn = Secondary_functions.create_connection_mysql_db(db_config["mysql"]["host"], 
                                        db_config["mysql"]["user"], 
                                        db_config["mysql"]["pass"],
                                        db_config["mysql"]["database"])
        cursor = conn.cursor()
        
        free_phone = random_number()
        count_user = db_call.check_user_phone(free_phone, cursor)

        while count_user >= 1:
            free_phone = random_number()
            count_user = db_call.check_user_phone(free_phone, cursor)
        cursor.close()
        conn.close()  
        print("Сгенерирован уникальный номер телефона")
        print("\nПодключение к MySQL завершено\n")

        return free_phone

    """Генерация уникального email"""
    def random_email():
        def random_email():
            random_email = str("".join([random.choice(list("1234567890")) for x in range(5)]) + "@ya.ru")
            return random_email
        
        conn = Secondary_functions.create_connection_mysql_db(db_config["mysql"]["host"], 
                                        db_config["mysql"]["user"], 
                                        db_config["mysql"]["pass"],
                                        db_config["mysql"]["database"])
        cursor = conn.cursor()
        
        free_email = random_email()
        count_user = db_call.check_user_email(free_email, cursor)

        while count_user >= 1:
            free_email = random_email()
            count_user = db_call.check_user_email(free_email, cursor)
        cursor.close()
        conn.close()  
        print("Сгенерирован уникальный email")
        print("\nПодключение к MySQL завершено\n")

        return free_email
