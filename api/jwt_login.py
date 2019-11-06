from .serializer import resident, securityGuard

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': resident.UserSerializer(user).data,
    }
def sjwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': securityGuard.SecuritySerializer(user).data,
    }