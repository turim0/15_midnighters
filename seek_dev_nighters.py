import requests
from datetime import datetime
from pytz import timezone
from collections import defaultdict


def load_attempts():
    url = 'http://devman.org/api/challenges/solution_attempts/'
    page = 1
    while True:
        response = requests.get(url, params={'page': page})
        if response.status_code == 404:
            break
        decoded_json = response.json()
        page += 1
        for record in decoded_json['records']:
            yield record


def get_midnighters():
    midnighters = defaultdict(list)
    for record in load_attempts():
        tz = timezone(record['timezone'])
        post_time = datetime.fromtimestamp(record['timestamp'], tz=tz)
        if post_time.hour in range(7):
            username = record['username']
            post_time = post_time.strftime('%d/%m/%y %H:%M')
            midnighters[username].append(post_time)
    return midnighters


def pprint(midnighters):
    for username, post_time in midnighters.items():
        print('-'*40)
        print('User: {} sent task at'.format(username))
        print('\n'.join(post_time))


if __name__ == '__main__':
    midnighters = get_midnighters()
    pprint(midnighters)
