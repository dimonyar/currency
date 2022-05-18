from accounts.tasks import new_users


def test_new_users(mailoutbox):
    new_users()
    assert mailoutbox[0].to == ['dy@rteam.net.ua']
    assert mailoutbox[0].subject == 'Count of Users of Currency-service achieved 1'
