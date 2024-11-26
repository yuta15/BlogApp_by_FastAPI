from fastapi.testclient import TestClient
import json
import os


with open(f'{os.getcwd()}/app/test/api/user/test_data.json', mode='r') as f:
    test_params = json.load(f)
url = 'http://localhost:8000/login'


def test_login_200(
    client: TestClient
):
    global url, test_params
    datas = test_params.get('user_data_login_200')
    for data in datas:
        form_data = {'username': data.get('username'), 'password': data.get('password')}
        res = client.post(url, data=form_data)
        assert 200 == res.status_code


def test_login_400(
    client: TestClient
):
    datas = test_params.get('user_data_login_400')
    for data in datas:
        form_data = {'username': data.get('username'), 'password': data.get('password')}
        res = client.post(url, data=form_data)
        assert 400 == res.status_code