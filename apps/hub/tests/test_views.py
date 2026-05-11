import pytest


@pytest.mark.django_db
class TestHomeView:
    def test_home_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_home_uses_correct_template(self, client):
        response = client.get("/")
        assert "hub/home.html" in [t.name for t in response.templates]
