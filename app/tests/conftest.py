from django.core.management import call_command

import pytest


@pytest.fixture(autouse=True, scope="function")   # noqa: PT003
def enable_db_access_for_all_tests(db):    # noqa: PT004
    """
    give access to database for all tests
    """


@pytest.fixture(autouse=True, scope="session")
def load_fixtures(django_db_setup, django_db_blocker):   # noqa: PT004
    with django_db_blocker.unblock():
        fixtures = (
            'source.json',
            'rate.json',
            'contactus.json',
            'user.json',
        )
        for fixture in fixtures:
            call_command('loaddata', f'tests/fixtures/{fixture}')   # noqa: PT004
