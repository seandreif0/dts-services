def test_healthz(client, secret_lookups):
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
    assert secret_lookups == []
