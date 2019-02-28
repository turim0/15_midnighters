import requests
from datetime import datetime
from pytz import timezone


def load_attempts():
    pages = 10
    for page in range(pages):
        response = requests.get(
            'http://devman.org/api/challenges/solution_attempts/?page='+str(page+1)
        )
        decoded_json = response.json()
        for record in decoded_json['records']:
            yield record


def get_midnighters():
    for record in load_attempts():
        tz = timezone(record['timezone'])
        post_time = datetime.fromtimestamp(record['timestamp'], tz=tz)
        if post_time.hour in range(7):
            username = record['username']
            post_time = post_time.strftime('%d/%m/%y %H:%M')
            print('{:<30}{:14}'.format(username, post_time))


if __name__ == '__main__':
    get_midnighters()
