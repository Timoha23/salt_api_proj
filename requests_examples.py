import requests


def _run(token, url, data_payload):
    headers = {
        'Accept': 'application/json',
        'X-Auth-Token': token,
    }
    response = requests.post(
        url=url,
        headers=headers,
        json=data_payload,
    )
    # print(response.text)
    return response


def _get_token(login_payload, url):
    headers = {'Accept': 'application/json'}
    token = requests.post(
        url + '/login',
        json=login_payload,
        headers=headers,
    )
    return token.json()['return'][0]['token']


########################################


def test_ping():
    token = _get_token(LOGIN_PAYLOAD, URL)
    data_payload = {
        'client': 'local_batch',
        'fun': 'test.ping',
        'tgt': '*',
        'batch': 1,
        'timeout': 120
    }
    result = _run(token, URL, data_payload)
    return result.json()


def run_custom_module():
    token = _get_token(LOGIN_PAYLOAD, URL)
    data_payload = {
        'client': 'local_batch',
        'fun': 'module_1.run',
        'tgt': '*',
        'batch': 1,
        'timeout': 120,
        'kwarg': {
            'start': 10,
            'end': 100
        }
    }
    result = _run(token, URL, data_payload)
    return result.json()


def run_custom_state():
    token = _get_token(LOGIN_PAYLOAD, URL)
    data_payload = {
        'client': 'local_batch',
        'fun': 'state.sls',
        'kwarg': {'mods': 'sls/states/run_modules'},
        'tgt': '*',
        'batch': 1,
        'timeout': 120
    }
    result = _run(token, URL, data_payload)
    return result.json()


def run_custom_runner():
    token = _get_token(LOGIN_PAYLOAD, URL)
    data_payload = {
        'client': 'runner',
        'fun': 'custom_runner.run',
        'arg': [1, 2, 3],
        'kwarg': {'1': 1, '2': 2}
    }
    result = _run(token, URL, data_payload)
    return result.json()


def run_custom_orch():
    token = _get_token(LOGIN_PAYLOAD, URL)
    data_payload = {
        'client': 'runner',
        'fun': 'state.orch',
        'arg': 'sls/orchestrate/run_modules',
    }
    result = _run(token, URL, data_payload)
    return result.json()


if __name__ == '__main__':
    LOGIN_PAYLOAD = {
        'username': '',
        'password': '',
        'eauth': 'file'
    }
    URL = 'http://<ip>:<port>'

    # print(test_ping())
    # print(run_custom_module())
    # print(run_custom_state())
    # print(run_custom_runner())
    # print(run_custom_orch())
