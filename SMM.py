import requests
import os
from dotenv import load_dotenv


def cut_link(token, original_url):
    params = {
        'v': '5.199',
        'access_token': token,
        'url': original_url,
        'private': 0
    }
    response = requests.get('https://api.vk.com/method/utils.getShortLink', params=params)
    response.raise_for_status()
    return response.json()


def count_clicks(token, url_key):
    params = {
        'v': '5.199',
        'access_token': token,
        'key': url_key,
        'interval': 'forever',
        'interval_counts': 'forever',
        'extended': 1
    }
    response = requests.get('https://api.vk.com/method/utils.getLinkStats', params=params)
    response.raise_for_status()
    return response.json()


def is_shorted_link(token, url_to_check):
    params = {
        'v': '5.199',
        'access_token': token,
        'url': url_to_check,
        'private': 0
    }
    response = requests.get('https://api.vk.com/method/utils.getShortLink', params=params)
    response.raise_for_status()
    short_url_data = response.json()
    return 'error' not in short_url_data and 'vk.cc/' in url_to_check


def main():
    try:
        load_dotenv()
        token = os.environ['VK_TOKEN']

        user_link = input('Введите ссылку ')

        if is_shorted_link(token, user_link):
            url_key = user_link.split('vk.cc/')[-1]
            link_stats_data = count_clicks(token, url_key)

            if 'error' in link_stats_data:
                print('Ошибка')
            else:
                views_count = link_stats_data["response"]["stats"][0]["views"]
                print(f'По ссылке перешло: {views_count}')
        else:
            short_url_response = cut_link(token, user_link)

            if 'error' in short_url_response:
                print('Ошибка')
            else:
                short_url_value = short_url_response['response']['short_url']
                print(f'Короткая ссылка: {short_url_value}')

    except requests.exceptions.HTTPError:
        print('Ошибка')
    except KeyError:
        print('Ошибка: VK_TOKEN не найден')


if __name__ == '__main__':
    main()
