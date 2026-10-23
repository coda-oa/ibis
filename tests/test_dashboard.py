from django.urls import reverse


def test_dashboard_returns_200(client):
    response = client.get(reverse("overview"))
    assert response.status_code == 200


def test_dashboard_shows_information_budget_heading(client):
    response = client.get(reverse("overview"))
    assert b"Information budget" in response.content
