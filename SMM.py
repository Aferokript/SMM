import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.environ['TOKEN']


def shorted_link(token, link):
    params = {
        'v': '5.199',
        'access_token': token,
        'url': link,
        'private': 0
    }

    try:
        response = requests.get('https://api.vk.com/method/utils.getShortLink', params=params)
        response.raise_for_status()
        data = response.json()
        if 'error' in data:
            return 'Ошибка'
        else:
            return data['response']['short_url']
    except requests.exceptions.HTTPError:
        return 'Ошибка'


def count_clicks(token, link):
    if 'vk.cc/' not in link:
        return 'Ошибка'

    key = link.split('vk.cc/')[-1]

    params = {
        'v': '5.199',
        'access_token': token,
        'key': key,
        'interval': 'forever',
        'interval_counts': 'forever',
        'extended': 1
    }

    try:
        response = requests.get('https://api.vk.com/method/utils.getLinkStats', params=params)
        response.raise_for_status()
        data_click = response.json()
        if 'error' in data_click:
            return 'Ошибка'
        else:
            views = data_click["response"]["stats"][0]["views"]
            return f'По ссылке перешло: {views}'
    except requests.exceptions.HTTPError:
        return 'Ошибка'


def is_shorted_link(link):
    return 'vk.cc/' in link


def main():
    user_link = input('Введите ссылку ')
    if is_shorted_link(user_link):
        print(count_clicks(token, user_link))
    else:
        result = shorted_link(token, user_link)
        if result != 'Ошибка':
            print(f'Короткая ссылка: {result}')
        else:
            print('Ошибка')


if __name__ == '__main__':
    main()