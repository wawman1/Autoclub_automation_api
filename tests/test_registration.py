from utils.api import Autoclub_api
from utils.cheking import Cheking
import allure

@allure.epic("Тесты регистрации")
class Test_registration():

    @allure.description("регистрация нового аккаунта")
    def test_register_user(self, base_url, db_cursor):

        with allure.step("Запрос кода на регистрацию"):
            sign_up = Autoclub_api.Authorization_registration_api.sign_up(base_url)
            Cheking.check_status_code(sign_up, 200)
            Cheking.check_json_keys(sign_up, ['otp_token', 'code'])

        with allure.step("Запрос на подтверждение кода регистрации"):
            phone_verify = Autoclub_api.Authorization_registration_api.phone_verify(sign_up.json().get("otp_token"), base_url, db_cursor)
            Cheking.check_status_code(phone_verify, 200)
            Cheking.check_json_keys(phone_verify, ['auth_token', 'user_cards'])
            Cheking.check_json_value(phone_verify, 'user_cards', False)

    
    @allure.description("Пользователь не указал имя")
    def test_register_invalid_name(self, base_url):

        with allure.step("Пользователь не указал имя"):
            sign_up = Autoclub_api.Authorization_registration_api.sign_up(base_url, name_user="")
            Cheking.check_status_code(sign_up, 422)
            Cheking.check_json_keys(sign_up, ['message', 'errors'])
            Cheking.check_error(sign_up, 'name',['Укажите имя'])

    @allure.description("Пользователь не указал номер телефона")
    def test_register_no_phone_number(self, base_url):

        with allure.step("Пользователь не указал номер телефона"):
            sign_up = Autoclub_api.Authorization_registration_api.sign_up(base_url, number="")
            Cheking.check_status_code(sign_up, 422)
            Cheking.check_json_keys(sign_up, ['message', 'errors'])
            Cheking.check_error(sign_up, 'phone',['Введите номер телефона'])
    
    @allure.description("Пользователь ввел недостаточное количество символов в поле для ввода номера телефона")
    def test_register_Invalid_number_format(self, base_url):

        with allure.step("Пользователь ввел недостаточное количество символов в поле для ввода номера телефона"):
            sign_up = Autoclub_api.Authorization_registration_api.sign_up(base_url, number="123")
            Cheking.check_status_code(sign_up, 422)
            Cheking.check_json_keys(sign_up, ['message', 'errors'])
            Cheking.check_error(sign_up, 'phone',['Неверный формат номера'])

    @allure.description("Пользователь с указанным номером телефона уже есть в базе данных")
    def test_register_error_used_phone(self, base_url):

        with allure.step("Пользователь с указанным номером телефона уже есть в базе данных"):
            sign_up = Autoclub_api.Authorization_registration_api.sign_up(base_url, number="79523211591")
            Cheking.check_status_code(sign_up, 422)
            Cheking.check_json_keys(sign_up, ['message', 'errors'])
            Cheking.check_error(sign_up, 'phone',['Учетная запись с таким номером уже существует'])



