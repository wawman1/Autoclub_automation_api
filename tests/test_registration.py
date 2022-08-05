import time
from utils.api import Autoclub_api
from utils.cheking import Cheking
import allure
from utils.request_db import db_call
import pytest

@allure.feature("Тесты регистрации")
@pytest.mark.registration
class Test_registration():
    
    @allure.story("Позитивные тесты регистрации")
    @pytest.mark.positive
    class Test_positive(): 

        @allure.title("регистрация нового аккаунта")
        def test_register_user(self, base_url, db_cursor):

            with allure.step("Запрос кода на регистрацию"):
                sign_up = Autoclub_api.Authorization_registration_api.sign_up(base_url)
                Cheking.check_status_code(sign_up, 200)
                Cheking.check_json_keys(sign_up, ['otp_token', 'code'])

            with allure.step("Запрос на подтверждение кода регистрации"):
                phone_verify = Autoclub_api.Authorization_registration_api.phone_verify(base_url, sign_up.json().get("otp_token"), db_cursor)
                Cheking.check_status_code(phone_verify, 200)
                Cheking.check_json_keys(phone_verify, ['auth_token', 'user_cards'])
                Cheking.check_json_value(phone_verify, 'user_cards', False)

            with allure.step("Получение данных профиля"):
                get_profile = Autoclub_api.Profile_api.profile(base_url, auth_token = 'Bearer ' + phone_verify.json().get("auth_token"))
                Cheking.check_status_code(get_profile, 200)
                Cheking.check_json_keys(get_profile, ['id', 'phone', 'name', 'email', 'birth_date'])

        @pytest.mark.expectation
        @allure.title("запрос на повторную отправку кода через 2 минуты и регистрация по полученному коду")
        def test_register_user_after_resend_otp_token(self, base_url):

            with allure.step("Запрос кода на регистрацию"):
                sign_up = Autoclub_api.Authorization_registration_api.sign_up(base_url)
                Cheking.check_status_code(sign_up, 200)
                Cheking.check_json_keys(sign_up, ['otp_token', 'code'])

            with allure.step("запрос на повторную отправку кода после истечения 2 минут"):
                otp_token = sign_up.json().get("otp_token")
                time.sleep(125)
                resend_code = Autoclub_api.Authorization_registration_api.resend_code(base_url, otp_token)
                Cheking.check_status_code(resend_code, 200)
                Cheking.check_json_keys(resend_code, ['code'])        
            
            with allure.step("Запрос на подтверждение кода регистрации"):
                phone_verify = Autoclub_api.Authorization_registration_api.phone_verify(base_url, otp_token, resend_code.json().get("code"))
                Cheking.check_status_code(phone_verify, 200)
                Cheking.check_json_keys(phone_verify, ['auth_token', 'user_cards'])
                Cheking.check_json_value(phone_verify, 'user_cards', False)
                
            with allure.step("Получение данных профиля"):
                get_profile = Autoclub_api.Profile_api.profile(base_url, auth_token = 'Bearer ' + phone_verify.json().get("auth_token"))
                Cheking.check_status_code(get_profile, 200)
                Cheking.check_json_keys(get_profile, ['id', 'phone', 'name', 'email', 'birth_date'])

    @allure.story("Негативные тесты регистрации")
    @pytest.mark.negativ
    class Test_negativ():
        @allure.title("Пользователь не указал имя")
        def test_register_invalid_name(self, base_url):

            with allure.step("Запрос кода на регистрацию без имени"):
                sign_up = Autoclub_api.Authorization_registration_api.sign_up(base_url, name_user="")
                Cheking.check_status_code(sign_up, 422)
                Cheking.check_json_keys(sign_up, ['message', 'errors'])
                Cheking.check_error(sign_up, 'name',['Укажите имя'])

        @allure.title("Пользователь не указал номер телефона")
        def test_register_no_phone_phone(self, base_url):

            with allure.step("Запрос кода на регистрацию без номера"):
                sign_up = Autoclub_api.Authorization_registration_api.sign_up(base_url, phone="")
                Cheking.check_status_code(sign_up, 422)
                Cheking.check_json_keys(sign_up, ['message', 'errors'])
                Cheking.check_error(sign_up, 'phone',['Введите номер телефона'])
        
        @allure.title("Пользователь ввел недостаточное количество символов в поле для ввода номера телефона")
        def test_register_invalid_phone_format(self, base_url):

            with allure.step("Запрос кода на регистрацию с коротким номером"):
                sign_up = Autoclub_api.Authorization_registration_api.sign_up(base_url, phone="123")
                Cheking.check_status_code(sign_up, 422)
                Cheking.check_json_keys(sign_up, ['message', 'errors'])
                Cheking.check_error(sign_up, 'phone',['Неверный формат номера'])

        @allure.title("Пользователь с указанным номером телефона уже есть в базе данных")
        def test_register_error_used_phone(self, base_url):

            with allure.step("Запрос кода на регистрацию с уже существующим номером в базе данных"):
                sign_up = Autoclub_api.Authorization_registration_api.sign_up(base_url, phone="79523211591")
                Cheking.check_status_code(sign_up, 422)
                Cheking.check_json_keys(sign_up, ['message', 'errors'])
                Cheking.check_error(sign_up, 'phone',['Учетная запись с таким номером уже существует'])

        @allure.title("Пользователь не ввел код подтверждения и нажал «Отправить»")
        def test_register_user_no_code(self, base_url):

            with allure.step("Запрос кода на регистрацию"):
                sign_up = Autoclub_api.Authorization_registration_api.sign_up(base_url)
                Cheking.check_status_code(sign_up, 200)
                Cheking.check_json_keys(sign_up, ['otp_token', 'code'])

            with allure.step("Запрос на подтверждение кода регистрации, без кода"):
                phone_verify = Autoclub_api.Authorization_registration_api.phone_verify(base_url, sign_up.json().get("otp_token"), "")
                Cheking.check_status_code(phone_verify, 422)
                Cheking.check_json_keys(phone_verify, ['message', 'errors'])
                Cheking.check_error(phone_verify, 'code',['Код введен неверно'])
        
        @allure.title("Пользователь указал недостаточное количество символов в поле для ввода кода и нажал «Отправить»")
        def test_register_user_short_code(self, base_url):

            with allure.step("Запрос кода на регистрацию"):
                sign_up = Autoclub_api.Authorization_registration_api.sign_up(base_url)
                Cheking.check_status_code(sign_up, 200)
                Cheking.check_json_keys(sign_up, ['otp_token', 'code'])

            with allure.step("Запрос на подтверждение кода регистрации, с кодом менее 6 символов"):
                phone_verify = Autoclub_api.Authorization_registration_api.phone_verify(base_url, sign_up.json().get("otp_token"), "123")
                Cheking.check_status_code(phone_verify, 422)
                Cheking.check_json_keys(phone_verify, ['message', 'errors'])
                Cheking.check_error(phone_verify, 'code',['Код введен неверно'])
                
        @allure.title("Пользователь указал неверный код и нажал «Отправить»")
        def test_register_user_invalid_code(self, base_url):

            with allure.step("Запрос кода на регистрацию"):
                sign_up = Autoclub_api.Authorization_registration_api.sign_up(base_url)
                Cheking.check_status_code(sign_up, 200)
                Cheking.check_json_keys(sign_up, ['otp_token', 'code'])

            with allure.step("Запрос на подтверждение кода регистрации, с не верным кодом"):
                phone_verify = Autoclub_api.Authorization_registration_api.phone_verify(base_url, sign_up.json().get("otp_token"), "123456")
                Cheking.check_status_code(phone_verify, 422)
                Cheking.check_json_keys(phone_verify, ['message', 'errors'])
                Cheking.check_error(phone_verify, 'code',['Код введен неверно'])
        
        @allure.title("Пользователь указал неверный otp_token")
        def test_register_user_invalid_otp_token(self, base_url):

            with allure.step("Запрос на подтверждение кода регистрации, с не верным otp_token"):
                phone_verify = Autoclub_api.Authorization_registration_api.phone_verify(base_url, "R5eb9EUsarwHauV6UIhe", "123456")
                Cheking.check_status_code(phone_verify, 422)
                Cheking.check_json_keys(phone_verify, ['message', 'errors'])
                Cheking.check_error(phone_verify, 'otp_token',['Указан недействительный временный пароль'])
        
        @pytest.mark.expectation
        @allure.title("Пользователь указал просроченный otp_token")
        def test_register_user_old_otp_token(self, base_url, db_cursor):

            with allure.step("Запрос кода на регистрацию"):
                sign_up = Autoclub_api.Authorization_registration_api.sign_up(base_url)
                Cheking.check_status_code(sign_up, 200)
                Cheking.check_json_keys(sign_up, ['otp_token', 'code'])

            with allure.step("Запрос на подтверждение кода регистрации, с просроченный otp_token"):
                otp_token = sign_up.json().get("otp_token")
                code = db_call.get_code(otp_token, db_cursor)
                time.sleep(125)
                phone_verify = Autoclub_api.Authorization_registration_api.phone_verify(base_url, otp_token, code)
                Cheking.check_status_code(phone_verify, 422)
                Cheking.check_json_keys(phone_verify, ['message', 'errors'])
                Cheking.check_error(phone_verify, 'code',['Код просрочен'])
        
        @allure.title("запрос на повторную отправку кода до истечения 2 минут")
        def test_register_user_resend_new_otp_token(self, base_url):

            with allure.step("Запрос кода на регистрацию"):
                sign_up = Autoclub_api.Authorization_registration_api.sign_up(base_url)
                Cheking.check_status_code(sign_up, 200)
                Cheking.check_json_keys(sign_up, ['otp_token', 'code'])

            with allure.step("запрос на повторную отправку кода до истечения 2 минут"):
                resend_code = Autoclub_api.Authorization_registration_api.resend_code(base_url, sign_up.json().get("otp_token"))
                Cheking.check_status_code(resend_code, 422)
                Cheking.check_json_keys(resend_code, ['message', 'errors'])
                Cheking.check_error(resend_code, 'otp_token',['Отправка кода возможна не чаще раза в 2 минуты'])
    
        @allure.title("запрос на повторную отправку кода по невалидному otp_token")
        def test_invalid_resend_otp_token(self, base_url):

            with allure.step("Запрос кода по не существующему otp_token"):
                resend_code = Autoclub_api.Authorization_registration_api.resend_code(base_url, "7cKp3pt7mdttiafJ1111")
                Cheking.check_status_code(resend_code, 422)
                Cheking.check_json_keys(resend_code, ['message', 'errors'])
                Cheking.check_error(resend_code, 'otp_token',['Указан недействительный временный пароль'])
