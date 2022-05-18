from currency.models import ContactUs

from django.urls import reverse


def test_contact_us_post_empty_data(client, mailoutbox):
    response = client.post(reverse('currency:contactus_create'))
    assert response.status_code == 200  # when post 200 is error
    assert len(mailoutbox) == 0
    assert response.context_data['form'].errors == {
        'subject': ['This field is required.'],
        'email_from': ['This field is required.'],
        'message': ['This field is required.'],
    }


def test_contact_us_post_valid_data(client, mailoutbox):
    initial_count = ContactUs.objects.count()

    payload = {
        'subject': 'Subject',
        'email_from': 'contact_email@example.com',
        'message': 'Example Text\n' * 10
    }

    response = client.post(reverse('currency:contactus_create'), data=payload)

    assert response.status_code == 302
    assert response.url == '/currency/contactus/'

    assert len(mailoutbox) == 1

    assert mailoutbox[0].from_email == payload['email_from']

    assert ContactUs.objects.count() == initial_count + 1


def test_rate_list(client):
    response = client.get(reverse('currency:rate_list'))
    assert response.status_code == 200


def test_rate_update(client):
    response = client.get('/currency/rate/update/145/')
    assert response.status_code == 302
    assert response.url == '/currency/rate/list'


def test_rate_delete(client):
    response = client.get('/currency/rate/delete/145/')
    assert response.status_code == 302
    assert response.url == '/currency/rate/list'
