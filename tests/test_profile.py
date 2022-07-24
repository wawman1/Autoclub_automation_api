from utils.api import Autoclub_api
from utils.cheking import Cheking
import allure

@allure.epic("Тесты профиля")
class Test_profile():

    with allure.step("Получение данных профиля"):
        def test_get_profile(self, base_url, auth_token):
                get_profile = Autoclub_api.Profile_api.profile(base_url, auth_token)
                Cheking.check_status_code(get_profile, 200)
                Cheking.check_json_keys(get_profile, ['id', 'phone', 'name', 'email', 'birth_date'])
                # Cheking.check_json_value(get_profile, 'id', 123)
    