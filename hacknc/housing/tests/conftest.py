from django.conf import settings
from django.utils import timezone
import factory
import pytest


class HostFactory(factory.django.DjangoModelFactory):
    address = 'here'
    guests_preferred = 8
    name = factory.Sequence(lambda n: f'Host {n}')
    tournament = factory.SubFactory('housing.tests.conftest.TournamentFactory')

    class Meta:
        model = 'housing.Host'


class TeamFactory(factory.django.DjangoModelFactory):
    arrival_time = factory.LazyFunction(timezone.now)
    name = factory.Sequence(lambda n: f'Team {n}')
    player_count = 21
    tournament = factory.SubFactory('housing.tests.conftest.TournamentFactory')

    class Meta:
        model = 'housing.Team'


class TournamentFactory(factory.django.DjangoModelFactory):
    date_end = factory.LazyFunction(timezone.now)
    date_lockout = factory.LazyFunction(timezone.now)
    date_start = factory.LazyFunction(timezone.now)
    location = 'here'
    name = factory.Sequence(lambda n: f'Tournament {n}')
    user = factory.SubFactory('housing.tests.conftest.UserFactory')

    class Meta:
        model = 'housing.Tournament'


class UserFactory(factory.django.DjangoModelFactory):
    name = 'John Smith'
    password = 'password'
    username = factory.Sequence(lambda n: f'user{n}')

    class Meta:
        model = settings.AUTH_USER_MODEL

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)

        return manager.create_user(*args, **kwargs)


@pytest.fixture
def host_factory(db):
    return HostFactory


@pytest.fixture
def team_factory(db):
    return TeamFactory


@pytest.fixture
def tournament_factory(db):
    return TournamentFactory


@pytest.fixture
def user_factory(db):
    return UserFactory
