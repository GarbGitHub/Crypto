from flask import session, request
import requests
import bs4 as bs4
from fake_useragent import UserAgent
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
        if location is None:
            return 'RU'
        else:
            return location['country_code']
    except Exception as e:
        print(e)
        return 'RU'


def user_ip():
    # result = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']
    # print('ip', result)
    # return result


# def yandex_internet() -> str:
#     """
#     The user's IP is determined using Yandex https://yandex.ru/internet/
#     :return: user ip, example RU '176.9.136.47'
#     """
#     host = requests.get('https://yandex.ru/internet/', headers={'User-Agent': UserAgent()['google chrome']})
#     ds = bs4.BeautifulSoup(host.text, "html.parser")
#     i = 0
#     ip = '176.9.136.47'
#     try:
#         ip_arr = ds.select(f".list-info__renderer")  # IPv4 or IPv6
#
#         while i != 2:
#             ip = ip_arr[i].getText()
#             if ip != 'не определен':
#                 break
#             i += 1
#         return ip
#
#     except IndexError:
#         print('ERROR: HTML document parsing error')
#         return ip
#
#     except Exception as e:
#         print(e)
#         return ip


def session_creation():
    session.permanent = True
    # session['ip'] = yandex_internet()
    session['ip'] = user_ip()
    session['country'] = country_definition(session['ip'])
    session['language'] = 'russian' if session['country'] == 'RU' else 'english'
    print('session_creation', session)


def session_del():
    """Удаление сессии"""
    print(session)
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
