from unittest import result
from urllib import response
from utils.api import Autoclub_api
from utils.cheking import Cheking

"""регистрация нового аккаунта"""

class Test_authorization_registration():

    def test_register_user(self):
        
        sign_up = Autoclub_api.sign_up()
        sign_up_json = sign_up.json()
        Cheking.check_status_code(sign_up, 200)
        phone_verify = Autoclub_api.phone_verify(sign_up_json)
        Cheking.check_status_code(phone_verify, 200)

