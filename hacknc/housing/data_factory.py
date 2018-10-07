import datetime

from django.utils import timezone

from housing import models


TOURNAMENT_DESCRIPTION = (
    "Event Type: Sanctioned Tournament - Sanctioned College Regular Season "
    "Tournament\nContact: Josh at jmnorris50@gmail.com"
)

TEAMS = (
    ('UNC', 31),
    ('Carleton College', 28),
    ('NC State', 27),
    ('Brown', 25),
    ('Wisconsin', 27),
)

HOSTS = (
    ('Smith', 16),
    ('James', 12),
    ('Young', 4),
    ('Carpenter', 8),
    ('Rodes', 10),
    ('Miller', 6),
    ('Brown', 20),
    ('Lee', 5),
    ('Davis', 12),
    ('Edwards', 15),
)


def create_dummy_data(user, tournament_name='Easterns'):
    now = timezone.now()
    start_date = now.date() + datetime.timedelta(days=30)
    end_date = start_date + datetime.timedelta(days=1)
    lockout_date = start_date - datetime.timedelta(days=7)

    tournament = models.Tournament.objects.create(
        date_end=end_date,
        date_lockout=lockout_date,
        date_start=start_date,
        description=TOURNAMENT_DESCRIPTION,
        location='150 Citizens Cir, Little River, SC 29566',
        name=tournament_name,
        user=user,
    )

    team_arrival_time = datetime.datetime.combine(
        start_date,
        datetime.time(hour=8),
    )

    for name, players in TEAMS:
        models.Team.objects.create(
            arrival_time=team_arrival_time,
            name=name,
            player_count=players,
            tournament=tournament,
            user=user,
        )

    for name, guests in HOSTS:
        models.Host.objects.create(
            address='The White House',
            email=f'{name}@example.com',
            guests_preferred=guests,
            name=name,
            phone_number='5555555555',
            tournament=tournament,
            user=user,
        )
