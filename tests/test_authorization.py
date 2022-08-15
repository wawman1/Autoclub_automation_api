import time
from utils.api import Autoclub_api
from utils.cheking import Cheking
import allure
from utils.request_db import db_call
import pytest
from conftest import Secondary_functions

@allure.feature("Тесты авторизации")
@pytest.mark.authorization
class Test_authorization():

    @allure.story("Позитивные тесты авторизации по номеру")
    @pytest.mark.positive
    class Test_positive_authorization_phone():
        @allure.title("Авторизация по номеру телефона")
        def test_authorization_user_phone(self, base_url, db_cursor, phone_user):

            with allure.step("Запрос кода на авторизацию"):
                sign_in = Autoclub_api.Authorization_registration_api.sign_in(base_url, phone_user)
                Cheking.check_status_code(sign_in, 200)
                Cheking.check_json_keys(sign_in, ['otp_token', 'code'])

            with allure.step("Запрос на подтверждение кода авторизации"):
                phone_verify = Autoclub_api.Authorization_registration_api.phone_verify(base_url, sign_in.json().get("otp_token"), db_cursor)
                Cheking.check_status_code(phone_verify, 200)
                Cheking.check_json_keys(phone_verify, ['auth_token', 'user_cards'])

            with allure.step("Получение данных профиля"):
                get_profile = Autoclub_api.Profile_api.profile(base_url, auth_token = 'Bearer ' + phone_verify.json().get("auth_token"))
                Cheking.check_status_code(get_profile, 200)
                Cheking.check_json_keys(get_profile, ['id', 'phone', 'name', 'email', 'birth_date'])
                
        @pytest.mark.expectation
        @allure.title("запрос на повторную отправку кода через 2 минуты и авторизацию по полученному коду")
        def test_register_user_after_resend_otp_token(self, base_url, phone_user):

            with allure.step("Запрос кода на авторизацию"):
                sign_in = Autoclub_api.Authorization_registration_api.sign_in(base_url, phone_user)
                Cheking.check_status_code(sign_in, 200)
                Cheking.check_json_keys(sign_in, ['otp_token', 'code'])

            with allure.step("запрос на повторную отправку кода после истечения 2 минут"):
                otp_token = sign_in.json().get("otp_token")
                time.sleep(125)
                resend_code = Autoclub_api.Authorization_registration_api.resend_code(base_url, otp_token)
                Cheking.check_status_code(resend_code, 200)
                Cheking.check_json_keys(resend_code, ['code'])        
            
            with allure.step("Запрос на подтверждение кода авторизации"):
                phone_verify = Autoclub_api.Authorization_registration_api.phone_verify(base_url, otp_token, resend_code.json().get("code"))
                Cheking.check_status_code(phone_verify, 200)
                Cheking.check_json_keys(phone_verify, ['auth_token', 'user_cards'])
                
            with allure.step("Получение данных профиля"):
                get_profile = Autoclub_api.Profile_api.profile(base_url, auth_token = 'Bearer ' + phone_verify.json().get("auth_token"))
                Cheking.check_status_code(get_profile, 200)
                Cheking.check_json_keys(get_profile, ['id', 'phone', 'name', 'email', 'birth_date'])
    
    @allure.story("Негативные тесты авторизации по номеру")
    @pytest.mark.negativ
    class Test_negativ_authorization_phone():
        @allure.title("Пользователь не указал номер телефона")
        def test_authorization_no_phone(self, base_url):

            with allure.step("Запрос кода на авторизацию без номера"):
                sign_in = Autoclub_api.Authorization_registration_api.sign_in(base_url, phone="")
                Cheking.check_status_code(sign_in, 422)
                Cheking.check_json_keys(sign_in, ['message', 'errors'])
                Cheking.check_error(sign_in, 'phone',['Номер телефона обязателен для заполнения'])
        
        @allure.title("Пользователь ввел недостаточное количество символов в поле для ввода номера телефона")
        def test_authorization_invalid_phone_format(self, base_url):

            with allure.step("Запрос кода на авторизацию с коротким номером"):
                sign_in = Autoclub_api.Authorization_registration_api.sign_in(base_url, phone="123")
                Cheking.check_status_code(sign_in, 422)
                Cheking.check_json_keys(sign_in, ['message', 'errors'])
                Cheking.check_error(sign_in, 'phone',['Неверный формат номера'])

        @allure.title("Пользователь с указанным номером телефона отсутствует")
        def test_authorization_error_used_phone(self, base_url):
            random_phone = Secondary_functions.random_phone()

            with allure.step("Запрос кода на авторизацию с номером которого нет в базе данных"):
                sign_in = Autoclub_api.Authorization_registration_api.sign_in(base_url, phone=random_phone)
                Cheking.check_status_code(sign_in, 422)
                Cheking.check_json_keys(sign_in, ['message', 'errors'])
                Cheking.check_error(sign_in, 'phone',['Учетная запись с таким номером отсутствует'])

        @allure.title("Пользователь не ввел код подтверждения и нажал «Отправить»")
        def test_authorization_user_no_code(self, base_url, phone_user):

            with allure.step("Запрос кода на авторизацию"):
                sign_in = Autoclub_api.Authorization_registration_api.sign_in(base_url, phone_user)
                Cheking.check_status_code(sign_in, 200)
                Cheking.check_json_keys(sign_in, ['otp_token', 'code'])

            with allure.step("Запрос на подтверждение кода авторизации, без кода"):
                phone_verify = Autoclub_api.Authorization_registration_api.phone_verify(base_url, sign_in.json().get("otp_token"), "")
                Cheking.check_status_code(phone_verify, 422)
                Cheking.check_json_keys(phone_verify, ['message', 'errors'])
                Cheking.check_error(phone_verify, 'code',['Код введен неверно'])
        
        @allure.title("Пользователь указал недостаточное количество символов в поле для ввода кода и нажал «Отправить»")
        def test_authorization_user_short_code(self, base_url, phone_user):

            with allure.step("Запрос кода на авторизацию"):
                sign_in = Autoclub_api.Authorization_registration_api.sign_in(base_url, phone_user)
                Cheking.check_status_code(sign_in, 200)
                Cheking.check_json_keys(sign_in, ['otp_token', 'code'])

            with allure.step("Запрос на подтверждение кода авторизации, с кодом менее 6 символов"):
                phone_verify = Autoclub_api.Authorization_registration_api.phone_verify(base_url, sign_in.json().get("otp_token"), "123")
                Cheking.check_status_code(phone_verify, 422)
                Cheking.check_json_keys(phone_verify, ['message', 'errors'])
                Cheking.check_error(phone_verify, 'code',['Код введен неверно'])
                
        @allure.title("Пользователь указал неверный код и нажал «Отправить»")
        def test_authorization_user_invalid_code(self, base_url, phone_user):

            with allure.step("Запрос кода на авторизацию"):
                sign_in = Autoclub_api.Authorization_registration_api.sign_in(base_url, phone_user)
                Cheking.check_status_code(sign_in, 200)
                Cheking.check_json_keys(sign_in, ['otp_token', 'code'])

            with allure.step("Запрос на подтверждение кода авторизации, с не верным кодом"):
                phone_verify = Autoclub_api.Authorization_registration_api.phone_verify(base_url, sign_in.json().get("otp_token"), "123456")
                Cheking.check_status_code(phone_verify, 422)
                Cheking.check_json_keys(phone_verify, ['message', 'errors'])
                Cheking.check_error(phone_verify, 'code',['Код введен неверно'])
        
        @allure.title("Пользователь указал неверный otp_token")
        def test_authorization_user_invalid_otp_token(self, base_url):

            with allure.step("Запрос на подтверждение кода авторизации, с не верным otp_token"):
                phone_verify = Autoclub_api.Authorization_registration_api.phone_verify(base_url, "R5eb9EUsarwHauV6UIhe", "123456")
                Cheking.check_status_code(phone_verify, 422)
                Cheking.check_json_keys(phone_verify, ['message', 'errors'])
                Cheking.check_error(phone_verify, 'otp_token',['Указан недействительный временный пароль'])
        
        @pytest.mark.expectation
        @allure.title("Пользователь указал просроченный otp_token")
        def test_authorization_user_old_otp_token(self, base_url, db_cursor, phone_user):

            with allure.step("Запрос кода на авторизацию"):
                sign_in = Autoclub_api.Authorization_registration_api.sign_in(base_url, phone_user)
                Cheking.check_status_code(sign_in, 200)
                Cheking.check_json_keys(sign_in, ['otp_token', 'code'])

            with allure.step("Запрос на подтверждение кода авторизации, с просроченный otp_token"):
                otp_token = sign_in.json().get("otp_token")
                code = db_call.get_code(otp_token, db_cursor)
                time.sleep(125)
                phone_verify = Autoclub_api.Authorization_registration_api.phone_verify(base_url, otp_token, code)
                Cheking.check_status_code(phone_verify, 422)
                Cheking.check_json_keys(phone_verify, ['message', 'errors'])
                Cheking.check_error(phone_verify, 'code',['Код просрочен'])
        
        @allure.title("запрос на повторную отправку кода до истечения 2 минут")
        def test_authorization_user_resend_new_otp_token(self, base_url, phone_user):

            with allure.step("Запрос кода на авторизацию"):
                sign_in = Autoclub_api.Authorization_registration_api.sign_in(base_url, phone_user)
                Cheking.check_status_code(sign_in, 200)
                Cheking.check_json_keys(sign_in, ['otp_token', 'code'])

            with allure.step("запрос на повторную отправку кода до истечения 2 минут"):
                resend_code = Autoclub_api.Authorization_registration_api.resend_code(base_url, sign_in.json().get("otp_token"))
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

    @allure.story("Позитивные тесты авторизации по email")
    @pytest.mark.positive
    class Test_positive_authorization_email():

        @allure.title("Авторизация по email")
        def test_authorization_email(self, base_url, auth_token, db_cursor):

            email = Secondary_functions.random_email()
            with allure.step("Добавление почты в профиль"):
                update_profile = Autoclub_api.Profile_api.profile_update(base_url, auth_token, email=email)
                Cheking.check_status_code(update_profile, 200)
                Cheking.check_json_keys(update_profile, ['id', 'phone', 'name', 'email', 'birth_date'])

            with allure.step("Запрос кода на авторизацию"):
                email_sign_in = Autoclub_api.Authorization_registration_api.email_sign_in(base_url, email)
                Cheking.check_status_code(email_sign_in, 200)
                Cheking.check_json_keys(email_sign_in, ['otp_token', 'code'])

            with allure.step("Запрос на подтверждение кода авторизации"):
                email_verify = Autoclub_api.Authorization_registration_api.email_verify(base_url, email_sign_in.json().get("otp_token"), db_cursor)
                Cheking.check_status_code(email_verify, 200)
                Cheking.check_json_keys(email_verify, ['auth_token', 'user_cards'])

            with allure.step("Получение данных профиля"):
                get_profile = Autoclub_api.Profile_api.profile(base_url, auth_token = 'Bearer ' + email_verify.json().get("auth_token"))
                Cheking.check_status_code(get_profile, 200)
                Cheking.check_json_keys(get_profile, ['id', 'phone', 'name', 'email', 'birth_date'])
                
        @pytest.mark.expectation
        @allure.title("запрос на повторную отправку кода через 2 минуты и авторизацию через email по полученному коду")
        def test_authorization_email_user_after_resend_otp_token(self, base_url, auth_token):

            email = Secondary_functions.random_email()
            with allure.step("Добавление почты в профиль"):
                update_profile = Autoclub_api.Profile_api.profile_update(base_url, auth_token, email=email)
                Cheking.check_status_code(update_profile, 200)
                Cheking.check_json_keys(update_profile, ['id', 'phone', 'name', 'email', 'birth_date'])

            with allure.step("Запрос кода на авторизацию"):
                email_sign_in = Autoclub_api.Authorization_registration_api.email_sign_in(base_url, email)
                Cheking.check_status_code(email_sign_in, 200)
                Cheking.check_json_keys(email_sign_in, ['otp_token', 'code'])

            with allure.step("запрос на повторную отправку кода после истечения 2 минут"):
                otp_token = email_sign_in.json().get("otp_token")
                time.sleep(610)
                resend_code = Autoclub_api.Authorization_registration_api.resend_code(base_url, otp_token)
                Cheking.check_status_code(resend_code, 200)
                Cheking.check_json_keys(resend_code, ['code'])        
            
            with allure.step("Запрос на подтверждение кода авторизации"):
                email_verify = Autoclub_api.Authorization_registration_api.email_verify(base_url, otp_token, resend_code.json().get("code"))
                Cheking.check_status_code(email_verify, 200)
                Cheking.check_json_keys(email_verify, ['auth_token', 'user_cards'])
                
            with allure.step("Получение данных профиля"):
                get_profile = Autoclub_api.Profile_api.profile(base_url, auth_token = 'Bearer ' + email_verify.json().get("auth_token"))
                Cheking.check_status_code(get_profile, 200)
                Cheking.check_json_keys(get_profile, ['id', 'phone', 'name', 'email', 'birth_date'])
    
    @allure.story("Негативные тесты авторизации по email")
    @pytest.mark.negativ
    class Test_negativ():
        @allure.title("Пользователь не указал email")
        def test_authorization_no_email(self, base_url):

            with allure.step("Запрос кода на авторизацию email"):
                email_sign_in = Autoclub_api.Authorization_registration_api.email_sign_in(base_url, email="")
                Cheking.check_status_code(email_sign_in, 422)
                Cheking.check_json_keys(email_sign_in, ['message', 'errors'])
                Cheking.check_error(email_sign_in, 'email',['Укажите адрес электронной почты'])
        
        @allure.title("Пользователь ввел недостаточное количество символов в поле для ввода email")
        def test_authorization_invalid_email_format(self, base_url):

            with allure.step("Запрос кода на авторизацию с коротким email"):
                email_sign_in = Autoclub_api.Authorization_registration_api.email_sign_in(base_url, email="123")
                Cheking.check_status_code(email_sign_in, 422)
                Cheking.check_json_keys(email_sign_in, ['message', 'errors'])
                Cheking.check_error(email_sign_in, 'email',['Некорректный адрес'])

        @allure.title("Пользователь с указанным email отсутствует")
        def test_authorization_error_used_email(self, base_url):

            with allure.step("Запрос кода на авторизацию с email которого нет в базе данных"):
                email_sign_in = Autoclub_api.Authorization_registration_api.email_sign_in(base_url, email=Secondary_functions.random_email())
                Cheking.check_status_code(email_sign_in, 422)
                Cheking.check_json_keys(email_sign_in, ['message', 'errors'])
                Cheking.check_error(email_sign_in, 'email',['Не найден пользователь с указанным адресом'])


        @allure.title("Пользователь не ввел код подтверждения и нажал «Отправить»")
        def test_authorization_email_user_no_code(self, base_url, auth_token):

            email = Secondary_functions.random_email()
            with allure.step("Добавление почты в профиль"):
                update_profile = Autoclub_api.Profile_api.profile_update(base_url, auth_token, email=email)
                Cheking.check_status_code(update_profile, 200)
                Cheking.check_json_keys(update_profile, ['id', 'phone', 'name', 'email', 'birth_date'])

            with allure.step("Запрос кода на авторизацию"):
                email_sign_in = Autoclub_api.Authorization_registration_api.email_sign_in(base_url, email)
                Cheking.check_status_code(email_sign_in, 200)
                Cheking.check_json_keys(email_sign_in, ['otp_token', 'code'])

            with allure.step("Запрос на подтверждение кода авторизации без кода"):
                email_verify = Autoclub_api.Authorization_registration_api.email_verify(base_url, email_sign_in.json().get("otp_token"), "")
                Cheking.check_status_code(email_verify, 422)
                Cheking.check_json_keys(email_verify, ['message', 'errors'])
                Cheking.check_error(email_verify, 'code',['Код введен неверно'])
        
        @allure.title("Пользователь указал недостаточное количество символов в поле для ввода кода и нажал «Отправить»")
        def test_authorization_email_user_short_code(self, base_url, auth_token):

            email = Secondary_functions.random_email()
            with allure.step("Добавление почты в профиль"):
                update_profile = Autoclub_api.Profile_api.profile_update(base_url, auth_token, email=email)
                Cheking.check_status_code(update_profile, 200)
                Cheking.check_json_keys(update_profile, ['id', 'phone', 'name', 'email', 'birth_date'])

            with allure.step("Запрос кода на авторизацию"):
                email_sign_in = Autoclub_api.Authorization_registration_api.email_sign_in(base_url, email)
                Cheking.check_status_code(email_sign_in, 200)
                Cheking.check_json_keys(email_sign_in, ['otp_token', 'code'])

            with allure.step("Запрос на подтверждение кода авторизации менее 6 символов"):
                email_verify = Autoclub_api.Authorization_registration_api.email_verify(base_url, email_sign_in.json().get("otp_token"), "1234")
                Cheking.check_status_code(email_verify, 422)
                Cheking.check_json_keys(email_verify, ['message', 'errors'])
                Cheking.check_error(email_verify, 'code',['Код введен неверно'])
                
        @allure.title("Пользователь указал неверный код и нажал «Отправить»")
        def test_authorization_email_user_invalid_code(self, base_url, auth_token):

            email = Secondary_functions.random_email()
            with allure.step("Добавление почты в профиль"):
                update_profile = Autoclub_api.Profile_api.profile_update(base_url, auth_token, email=email)
                Cheking.check_status_code(update_profile, 200)
                Cheking.check_json_keys(update_profile, ['id', 'phone', 'name', 'email', 'birth_date'])

            with allure.step("Запрос кода на авторизацию"):
                email_sign_in = Autoclub_api.Authorization_registration_api.email_sign_in(base_url, email)
                Cheking.check_status_code(email_sign_in, 200)
                Cheking.check_json_keys(email_sign_in, ['otp_token', 'code'])

            with allure.step("Запрос на подтверждение кода авторизации с не верным кодом"):
                email_verify = Autoclub_api.Authorization_registration_api.email_verify(base_url, email_sign_in.json().get("otp_token"), "123456")
                Cheking.check_status_code(email_verify, 422)
                Cheking.check_json_keys(email_verify, ['message', 'errors'])
                Cheking.check_error(email_verify, 'code',['Код введен неверно'])
        
        @allure.title("Пользователь указал неверный otp_token")
        def test_authorization_email_user_invalid_otp_token(self, base_url):

            with allure.step("Запрос на подтверждение кода авторизации, с не верным otp_token"):
                email_verify = Autoclub_api.Authorization_registration_api.email_verify(base_url, "R5eb9EUsarwHauV6UIhe", "123456") # код по правильнопу сделать верным, не нужно хардкодить токен
                Cheking.check_status_code(email_verify, 422)
                Cheking.check_json_keys(email_verify, ['message', 'errors'])
                Cheking.check_error(email_verify, 'otp_token',['Указан недействительный временный пароль'])
        
        @pytest.mark.expectation
        @allure.title("Пользователь указал просроченный otp_token")
        def test_authorization_email_user_old_otp_token(self, base_url, db_cursor, auth_token):

            email = Secondary_functions.random_email()
            with allure.step("Добавление почты в профиль"):
                update_profile = Autoclub_api.Profile_api.profile_update(base_url, auth_token, email=email)
                Cheking.check_status_code(update_profile, 200)
                Cheking.check_json_keys(update_profile, ['id', 'phone', 'name', 'email', 'birth_date'])

            with allure.step("Запрос кода на авторизацию"):
                email_sign_in = Autoclub_api.Authorization_registration_api.email_sign_in(base_url, email)
                Cheking.check_status_code(email_sign_in, 200)
                Cheking.check_json_keys(email_sign_in, ['otp_token', 'code'])

            with allure.step("Запрос на подтверждение кода авторизации, с просроченный otp_token"):
                otp_token = email_sign_in.json().get("otp_token")
                code = db_call.get_code(otp_token, db_cursor)
                time.sleep(610)
                email_verify = Autoclub_api.Authorization_registration_api.email_verify(base_url, otp_token, code)
                Cheking.check_status_code(email_verify, 422)
                Cheking.check_json_keys(email_verify, ['message', 'errors'])
                Cheking.check_error(email_verify, 'code',['Код просрочен'])

        @allure.title("запрос на повторную отправку кода до истечения 10 минут")
        def test_authorization_email_user_resend_new_otp_token(self, base_url, auth_token):

            email = Secondary_functions.random_email()
            with allure.step("Добавление почты в профиль"):
                update_profile = Autoclub_api.Profile_api.profile_update(base_url, auth_token, email=email)
                Cheking.check_status_code(update_profile, 200)
                Cheking.check_json_keys(update_profile, ['id', 'phone', 'name', 'email', 'birth_date'])

            with allure.step("Запрос кода на авторизацию"):
                email_sign_in = Autoclub_api.Authorization_registration_api.email_sign_in(base_url, email)
                Cheking.check_status_code(email_sign_in, 200)
                Cheking.check_json_keys(email_sign_in, ['otp_token', 'code'])

            with allure.step("запрос на повторную отправку кода до истечения 10 минут"):
                otp_token = email_sign_in.json().get("otp_token")
                resend_code = Autoclub_api.Authorization_registration_api.resend_code(base_url, otp_token)
                Cheking.check_status_code(resend_code, 422)
                Cheking.check_json_keys(resend_code, ['message', 'errors'])
                Cheking.check_error(resend_code, 'otp_token',['Отправка кода возможна не чаще раза в 10 минуты'])  
    
        @allure.title("запрос на повторную отправку кода по невалидному otp_token")
        def test_invalid_resend_otp_token(self, base_url):

            with allure.step("Запрос кода по не существующему otp_token"):
                resend_code = Autoclub_api.Authorization_registration_api.resend_code(base_url, "7cKp3pt7mdttiafJ1111") # токен не нужо хардкодить
                Cheking.check_status_code(resend_code, 422)
                Cheking.check_json_keys(resend_code, ['message', 'errors'])
                Cheking.check_error(resend_code, 'otp_token',['Указан недействительный временный пароль'])