from currency.models import ContactUs

from django.urls import reverse


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
