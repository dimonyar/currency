from django.urls import reverse

from rest_framework.test import APIClient


def test_contactus_get_list():
    client = APIClient()
    response = client.get(reverse('api:contactus-list'))
    assert response.status_code == 200

