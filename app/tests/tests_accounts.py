from accounts.models import User

from django.urls import reverse


def test_login_empty_data(client):
    response = client.post('/accounts/login/')
    assert response.status_code == 200  # when post 200 is error
    assert response.context_data['form'].errors == {
        'username': ['This field is required.'],
        'password': ['This field is required.']
    }


def test_login_invalid_data(client):
    payload = {
        'username': 'dyrteam.net.ua',
        'password': '1',
    }
    response = client.post('/accounts/login/', data=payload)
    assert response.status_code == 200
    assert response.context_data['form'].errors['__all__'] == [
        'Please enter a correct email address and password. Note that both fields may be case-sensitive.'
    ]


def test_login_valid_data(client):
    payload = {
        'username': 'dy@rteam.net.ua',
        'password': '1'
    }
    response = client.post('/accounts/login/', data=payload)
    assert response.status_code == 302
    assert response.url == '/'

    # My Profile
    response = client.get(reverse('accounts:my-profile'))
    assert response.status_code == 200
    assert User.objects.get(email='dy@rteam.net.ua').phone == '380672567178'

    payload = {
        'first_name': 'Dmitry',
        'last_name': 'Yaroshevsky',
        'phone': '+380 (67) 256-71-73',
        'avatar': ''
    }
    response = client.post(reverse('accounts:my-profile'), data=payload)
    assert User.objects.get(email='dy@rteam.net.ua').phone == '380672567173'
    assert response.status_code == 302
    assert response.url == '/'


def test_signup_epmpty_data(client, mailoutbox):
    response = client.post(reverse('accounts:signup'))
    assert response.context_data['form'].errors == {
        'email': ['This field is required.'],
        'password': ['This field is required.'],
        'confirm': ['This field is required.']
    }
    assert response.status_code == 200
    assert len(mailoutbox) == 0


def test_signup_invalid_confirm_data(client, mailoutbox):
    payload = {
        'email': 'info@rteam.net.ua',
        'password': '1',
        'confirm': '2',
    }
    response = client.post(reverse('accounts:signup'), data=payload)

    assert response.context_data['form'].errors['__all__'] == ['Passwords should match!']
    assert response.status_code == 200
    assert len(mailoutbox) == 0


def test_signup_valid_data(client, mailoutbox):
    payload = {
        'email': 'info@rteam.net.ua',
        'password': '1',
        'confirm': '1',
    }
    response = client.post(reverse('accounts:signup'), data=payload)

    assert response.status_code == 302
    assert len(mailoutbox) == 1
    assert mailoutbox[0].to == [payload['email']]
    assert mailoutbox[0].subject == 'Sign Up'
    link = mailoutbox[0].body.replace('\n', '').split(' ')[25]
    assert User.objects.get(email=payload['email']).is_active is False

    # Account is activated!
    response = client.get(link)
    assert response.status_code == 302
    assert response.url == '/accounts/login/'
    assert User.objects.get(email=payload['email']).is_active is True

    # Account already activated!
    response = client.get(link)
    assert response.status_code == 302
    assert response.url == '/accounts/login/'
