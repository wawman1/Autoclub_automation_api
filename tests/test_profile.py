from utils.api import Autoclub_api
from utils.cheking import Cheking
import allure
from conftest import Secondary_functions
import pytest

@allure.epic("Тесты профиля")
@pytest.mark.profile
class Test_profile():

    @allure.story("Позитивные тесты профиля")
    @pytest.mark.positive
    class Test_positive_profile():

        def test_get_profile(self, base_url, auth_token):

            with allure.step("Получение данных профиля"):
                get_profile = Autoclub_api.Profile_api.profile(base_url, auth_token)
                Cheking.check_status_code(get_profile, 200)
                Cheking.check_json_keys(get_profile, ['id', 'phone', 'name', 'email', 'birth_date'])
        
        def test_profile_update(self, base_url, auth_token):

                with allure.step("Добавление email в профиль"):
                    update_profile = Autoclub_api.Profile_api.profile_update(base_url, auth_token, email=Secondary_functions.random_email())
                    Cheking.check_status_code(update_profile, 200)
                    Cheking.check_json_keys(update_profile, ['id', 'phone', 'name', 'email', 'birth_date'])
        
    # @allure.story("Негативные тесты профиля")
    # @pytest.mark.negativ
    # class Test_positive_profile():

        