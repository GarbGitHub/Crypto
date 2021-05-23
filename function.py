from flask import session, request

from ipstack import GeoLookup
from config import KEY_STACK


def country_definition(ip: str) -> str:
    """
    :param ip: user's IP
    :return: country
    """
    geo_lookup = GeoLookup(KEY_STACK)
    try:
        location = geo_lookup.get_location(ip)
        print(location)
        return location['country_code'] if location['country_code'] else 'RU'
    except Exception as e:
        print(e)
        return 'RU'


def user_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']


def session_creation():
    session.permanent = True
    session['ip'] = user_ip()
    session['country'] = country_definition(session['ip'])
    if session['country'] == 'RU':
        session['language'] = 'Russian'
    elif session['country'] == 'ES':
        session['language'] = 'Spanish'
    else:
        session['language'] = 'English'


def session_del():
    """Удаление сессии"""
    session.permanent = False
    session.pop('ip', None)
    session.pop('country', None)
    session.pop('language', None)
    return f'сессия удалена: {session}'


def check_session():
    if 'ip' in session and 'country' in session and 'language' in session:
        return True
    else:
        return False
