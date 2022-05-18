from .models import UserToken
import secrets
import base64
import uuid
import json

from .serializers import UserData


def generate_token(data):
    user = data.get('user')
    user_data = json.dumps(UserData(user).data)
    user_data = user_data.encode('ascii')
    user_data = base64.b64encode(user_data).decode('utf-8')
    token = f"{uuid.uuid4()}-{secrets.token_hex()}-{user_data}"
    try:
        UserToken.objects.create(user=user, token=token)
    except:
        UserToken.objects.filter(user=user).update(token=token)
    return token


def authenticate_token(data):
    token = data.get('token')
    user_id = data.get('user_id')
    try:
        UserToken.objects.get(token=token, user_id=user_id)
        user_data = json.loads(base64.b64decode(token.split('-')[-1]).decode('utf-8'))
        return True, user_data
    except Exception as e:
        return False, f"{e}"
