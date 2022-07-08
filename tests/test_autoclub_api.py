from utils.api import Autoclub_api
from utils.cheking import Cheking

"""регистрация нового аккаунта"""

class Test_authorization_registration():

    def test_register_user(self):
        
        sign_up = Autoclub_api.sign_up()
        Cheking.check_status_code(sign_up, 200)
        Cheking.check_json_keys(sign_up, ['otp_token', 'code'])
        phone_verify = Autoclub_api.phone_verify(sign_up.json())
        Cheking.check_status_code(phone_verify, 200)
        Cheking.check_json_keys(phone_verify, ['auth_token', 'user_cards'])
        Cheking.check_json_value(phone_verify, 'user_cards', False)
        # print(list(phone_verify.json()))

