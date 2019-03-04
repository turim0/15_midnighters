import requests
from datetime import datetime
from pytz import timezone
from collections import defaultdict


def load_attempts():
    url = 'http://devman.org/api/challenges/solution_attempts/'
    page = 1
    while True:
        response = requests.get(url, params={'page': page})
        decoded_json = response.json()
        page += 1
        if decoded_json['number_of_pages'] == page:
            break
        yield from decoded_json['records']


def get_midnighters(attempts):
    midnighters = defaultdict(list)
    for attempt in attempts:
        tz = timezone(attempt['timezone'])
        post_time = datetime.fromtimestamp(attempt['timestamp'], tz=tz)
        if post_time.hour in range(7):
            username = attempt['username']
            post_time = post_time.strftime('%d/%m/%y %H:%M')
            midnighters[username].append(post_time)
    return midnighters


def pprint(midnighters):
    for username, post_time in midnighters.items():
        print('-'*40)
        print('User: {} sent task at'.format(username))
        print('\n'.join(post_time))


if __name__ == '__main__':
    midnighters = get_midnighters(load_attempts())
    pprint(midnighters)
