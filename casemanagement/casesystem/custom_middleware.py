import jwt
from django.contrib.auth.middleware import AuthenticationMiddleware

salt = "qwertyuiop"


def get_verify_jwt_token(encode_string, decoded_string=None, is_for_decode=False):
    if not is_for_decode:
        encoded = jwt.encode({'_auth_user': encode_string}, salt, algorithm='HS256')
        return str(encoded)
    decoded = jwt.decode(decoded_string, salt, algorithms=['HS256'])
    if decoded == {'_auth_user': encode_string}:
        print(decoded)
        return True
    return False


class CustomMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        super(CustomMiddleware, self).process_request(request)
        setattr(request, 'role', 0)
        user = request.user
        if user and hasattr(user, 'userrole'):
            setattr(request, 'role', user.userrole.role)

        # if user and not isinstance(user, AnonymousUser):
        #     if hasattr(user, 'userrole'):
        #         if not request.session.has_key('_auth_user'):
        #             request.session['_auth_user'] = get_verify_jwt_token(
        #                 encode_string=user.token_secret_key,
        #             )
        #         setattr(request, 'role', user.userrole.role)
        #         # else:
        #         #     auth_hash = request.session['_auth_user']
        #         #     if auth_hash:
        #         #         verify_token = get_verify_jwt_token(
        #         #             username,
        #         #             auth_hash,
        #         #             True
        #         #         )
        #         #         if verify_token:
        #         #             setattr(request, 'role', user.userrole.role)

