from propelauth_py import init_base_auth, UnauthorizedException
from decouple import config

auth_url = config("auth_url")
api_key = config("api_key")

class PropelAuth:
    def __init__(self):
        self.auth = init_base_auth(auth_url, api_key)
    
    def checkUser(self, auth_header):
        try:
            user = self.auth.validate_access_token_and_get_user(auth_header)
        except UnauthorizedException:
            return False
        return user.user_id