from fastapi.testclient import TestClient
import json
import os


with open(f'{os.getcwd()}/app/test/api/user/test_data.json', mode='r') as f:
    register_test_params = json.load(f)
url = 'http://localhost:8000/user/register'

# success
def test_user_register_200(
    client: TestClient
):
    """
    ユーザー情報の追加
    """
    global url, register_test_params
    for param_200 in register_test_params.get('user_data_register_200'):
        response = client.post(url=url, json=param_200)
        assert 200 == response.status_code


def test_user_register_400(
    client: TestClient
):
    """
    validation Error が発生した際には、400 Bad Requestが送信されることを確認する。
    """
    global url, register_test_params
    for param_400 in register_test_params.get('user_data_register_400'):
        response = client.post(url=url, json=param_400)
        assert 400 == response.status_code
    

# conflict
def test_user_register_409(
    client: TestClient
):
    """
    DB内に重複したデータを送信した際には、409 conflictを送信するようにする。
    """
    global url, register_test_params
    for param_409 in register_test_params.get('user_data_register_409'):
        response = client.post(url=url, json=param_409)
        assert 409 == response.status_code