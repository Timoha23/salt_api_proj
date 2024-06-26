import requests


def test_ping(token, url):
    headers = {
        'Accept': 'application/json',
        'X-Auth-Token': token,
    }
    data_payload = {
        'client': 'local',
        'tgt': '*',
        'fun': 'test.ping'
    }
    response = requests.post(
        url=url,
        headers=headers,
        json=data_payload,
    )
    return response.json()


def get_token(login_payload, url):
    headers = {'Accept': 'application/json'}
    token = requests.post(
        url + '/login',
        json=login_payload,
        headers=headers
    )
    return token.json()['return'][0]['token']


if __name__ == '__main__':
    login_payload = {
        'username': '',
        'password': '',
        'eauth': 'file'
    }
    url = 'https://<ip>:<port>'
    token = get_token(login_payload, url)
    ping_result = test_ping(token, url)
    print(ping_result)
