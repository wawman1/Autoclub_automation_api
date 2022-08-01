import time
from utils.api import Autoclub_api
from utils.cheking import Cheking
import allure
from utils.request_db import db_call
import pytest

@allure.feature("Тесты авторизации")
@pytest.mark.registration
class Test_authorization():


    @allure.story("Позитивные тесты авторизации")
    @pytest.mark.positive
    class Test_positive():
        @allure.description("Авторизация по номеру телефона")
        def test_authorization_user_phone(self, base_url, db_cursor, phone_user):

            with allure.step("Запрос кода на авторизацию"):
                sign_up = Autoclub_api.Authorization_registration_api.sign_in(base_url, phone_user)
                Cheking.check_status_code(sign_up, 200)
                Cheking.check_json_keys(sign_up, ['otp_token', 'code'])

            with allure.step("Запрос на подтверждение кода авторизации"):
                phone_verify = Autoclub_api.Authorization_registration_api.phone_verify(base_url, sign_up.json().get("otp_token"), db_cursor)
                Cheking.check_status_code(phone_verify, 200)
                Cheking.check_json_keys(phone_verify, ['auth_token', 'user_cards'])

            with allure.step("Получение данных профиля"):
                get_profile = Autoclub_api.Profile_api.profile(base_url, auth_token = 'Bearer ' + phone_verify.json().get("auth_token"))
                Cheking.check_status_code(get_profile, 200)
                Cheking.check_json_keys(get_profile, ['id', 'phone', 'name', 'email', 'birth_date'])
    
    # @allure.story("Негативные тесты авторизации")
    # @pytest.mark.negativ
    # class Test_negativ():

