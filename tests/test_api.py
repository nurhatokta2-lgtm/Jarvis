from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint():
    client = TestClient(app)
    res = client.get('/api/health')
    assert res.status_code == 200
    assert res.json()['status'] == 'ok'


def test_chat_without_voice():
    client = TestClient(app)
    res = client.post('/api/chat', json={'session_id': 't1', 'message': 'hello', 'use_voice': False})
    assert res.status_code == 200
    body = res.json()
    assert 'answer' in body
    assert body['audio_url'] is None
