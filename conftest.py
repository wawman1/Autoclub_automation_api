import pytest
import random
from utils.http_methods import Http_method
import mysql.connector
from mysql.connector import Error
from config import db_config 

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

"""Регистрация нового пользователя и выдача его токена, один тестовый пользователь на сессию"""
@pytest.fixture(scope="session")    
def auth_token(base_url):
    print("\n\nПодготовка тестового аккаунта")
    random_number = ''.join([random.choice(list('1234567890')) for x in range(10)])
    json_for_sign_up = {
        "phone": "7" + random_number,
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
@pytest.fixture(scope="session") 
def db_cursor():
    def create_connection_mysql_db(db_host, user_name, user_password, db_name = None):
        connection_db = None
        try:
            connection_db = mysql.connector.connect(
                host = db_host,
                user = user_name,
                passwd = user_password,
                database = db_name
            )
            print("Подключение к MySQL успешно выполнено\n\n")
        except Error as db_connection_error:
            print("Возникла ошибка: ", db_connection_error)
        return connection_db
        
    conn = create_connection_mysql_db(db_config["mysql"]["host"], 
                                    db_config["mysql"]["user"], 
                                    db_config["mysql"]["pass"],
                                    db_config["mysql"]["database"])
    cursor = conn.cursor()
    yield cursor
    cursor.close()
    conn.close()  
    print("\n\nПодключение к MySQL завершено")