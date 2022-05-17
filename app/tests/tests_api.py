from currency.models import ContactUs

from django.urls import reverse


def test_contactus_get_list(api_client):
    response = api_client.get(reverse('api:contactus-list'))
    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'email_from': 'd.yaroshevsky@gmail.com', 'subject': 'Test subject', 'message': 'Test Message'},
        {'id': 21, 'email_from': 'task_api@gmail.com', 'subject': 'API created task',
         'message': 'Use send mail new contactus'}
    ]


def test_contactus_post_empty_data(api_client):
    response = api_client.post(reverse('api:contactus-list'), data={})
    assert response.status_code == 400
    assert response.json() == {
        'email_from': ['This field is required.'],
        'subject': ['This field is required.'],
        'message': ['This field is required.']
    }


def test_contactus_post_valid_data(api_client):
    payload = {
        'email_from': 'info@currency.com',
        'subject': 'Pytest subject',
        'message': 'Pytest message'
    }
    response = api_client.post(reverse('api:contactus-list'), data=payload)
    assert response.status_code == 201
    assert response.json()['email_from'] == payload['email_from']
    assert response.json()['subject'] == payload['subject']
    assert response.json()['message'] == payload['message']


def test_contactus_post_invalid_email(api_client):
    payload = {
        'email_from': 'info#currency.com',
        'subject': 'Pytest subject',
        'message': 'Pytest message'
    }
    response = api_client.post(reverse('api:contactus-list'), data=payload)
    assert response.status_code == 400
    assert response.json() == {
        'email_from': ['Enter a valid email address.']
    }


def test_contactus_patch_valid_data(api_client):
    last_contact = ContactUs.objects.last()
    payload = {
        'subject': 'Patch subject',
    }
    response = api_client.patch(reverse('api:contactus-detail', args=[last_contact.id]), data=payload)
    assert response.status_code == 200
    assert response.json()['id'] == last_contact.id
    assert response.json()['subject'] == payload['subject']


def test_contactus_put_valid_data(api_client):
    last_contact = ContactUs.objects.last()
    payload = {
        'email_from': 'put@currency.com',
        'subject': 'PUT subject',
        'message': 'PUT message'
    }
    response = api_client.put(reverse('api:contactus-detail', args=[last_contact.id]), data=payload)
    assert response.status_code == 200
    assert response.json()['email_from'] == payload['email_from']
    assert response.json()['subject'] == payload['subject']
    assert response.json()['message'] == payload['message']


def test_contactus_delete(api_client):
    count_contact = ContactUs.objects.count()
    last_contact = ContactUs.objects.last()
    response = api_client.delete(reverse('api:contactus-detail', args=[last_contact.id]))
    assert response.status_code == 204
    assert count_contact == ContactUs.objects.count() + 1
