from fastapi.testclient import TestClient


def test_user_register(
    client: TestClient
):
    url = 'http://localhost:8000/user/register'
    data = {
        'username': 'user04',
        'email': 'user04@example.com',
        'plain_password': 'user04password'
    }
    
    response = client.post(url=url, json=data)
    assert 200 == response.status_code