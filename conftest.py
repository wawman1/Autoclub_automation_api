import pytest
import random
from utils.http_methods import Http_method


def pytest_addoption(parser):
    parser.addoption('--server', action='store', default="dev",
                     help="Выберите сервер на котором нужно запускать тесты\n доступные варианты: dev")



@pytest.fixture(scope="session")    
def base_url(request):
    server_name = request.config.getoption('server')
    if server_name == "dev":
        print("\nstart server dev for test..")
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

@pytest.fixture(scope="session")    
def creat_account(base_url):
    random_number = ''.join([random.choice(list('1234567890')) for x in range(10)])
    json_for_sign_up = {
        "phone": "7" + random_number,
        "name": "autotest"
    }

    post_resource_sign_up = "/auth/phone/sign-up"
    post_resource_sign_up_url = base_url + post_resource_sign_up
    
    result_sign_up = Http_method.post(post_resource_sign_up_url, json_for_sign_up)
    result_sign_up.encoding = "utf-8"
    reaspons_sign_up = result_sign_up.json()

    post_resource_phone_verify = "/auth/phone/verify"
    post_resource_phone_verify_url = base_url + post_resource_phone_verify

    result_phone_verify = Http_method.post(post_resource_phone_verify_url, reaspons_sign_up)
    result_phone_verify.encoding = "utf-8"
    auth_token = 'Bearer ' + result_phone_verify.json().get("auth_token")
    return auth_token