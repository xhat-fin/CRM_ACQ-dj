import jwt
from datetime import datetime, timedelta
import requests as req
from flask import session
from random import randint


def check_token(access, refresh):
    try:
        data_ac_token = jwt.decode(access, options={"verify_signature": False})
        data_re_token = jwt.decode(refresh, options={"verify_signature": False})
    except:
        return False
    date_now = datetime.now()
    if date_now < datetime.fromtimestamp(data_ac_token.get('exp')):
        print('ACCESS токен валидный')
        return True
    elif date_now < datetime.fromtimestamp(data_re_token.get('exp')):
        new_ac_token = req.post('http://127.0.0.1:8000/auth/api/token/refresh/', json={"refresh": refresh})
        new_ac_token = new_ac_token.json()
        session['access'] = new_ac_token.get('access')
        session['refresh'] = new_ac_token.get('refresh')
        print('заменили с помощью refresh access')
        return True
    else:
        print('Все просрочено')
        return False


print()
