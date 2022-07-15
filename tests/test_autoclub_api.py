from utils.api import Autoclub_api
from utils.cheking import Cheking
import allure

@allure.epic("Тесты регистрации и авторизации")
class Test_authorization_registration():

    @allure.description("регистрация нового аккаунта")
    def test_register_user(self, base_url, db_cursor):

        with allure.step("Запрос кода на регистрацию"):
            sign_up = Autoclub_api.sign_up(base_url)
            Cheking.check_status_code(sign_up, 200)
            Cheking.check_json_keys(sign_up, ['otp_token', 'code'])

        with allure.step("Запрос на подтверждение кода регистрации"):
            phone_verify = Autoclub_api.phone_verify(sign_up.json().get("otp_token"), base_url, db_cursor)
            Cheking.check_status_code(phone_verify, 200)
            Cheking.check_json_keys(phone_verify, ['auth_token', 'user_cards'])
            Cheking.check_json_value(phone_verify, 'user_cards', False)

@allure.epic("Тесты профиля")
class Test_profile():

    with allure.step("Получение данных профиля"):
        def test_get_profile(self, base_url, creat_account):
                get_profile = Autoclub_api.profile(base_url, creat_account)
                Cheking.check_status_code(get_profile, 200)
                Cheking.check_json_keys(get_profile, ['id', 'phone', 'name', 'email', 'birth_date'])
                # Cheking.check_json_value(get_profile, 'id', 123)
        

