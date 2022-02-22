from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_quotes_main():
    tag = 'world'
    world_quotes = [
        {
            "text": "The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.",
            "author": "Albert Einstein"
        }
    ]
    response = client.get(f"/quotes/{tag}")
    assert response.status_code == 200
    assert response.json() == world_quotes