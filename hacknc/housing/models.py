import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


def generate_slug_key():
    """
    Generate a short, random string to guarantee uniqueness of a slug.

    Returns:
        A 6 character random string.
    """
    return get_random_string(length=6)


class Host(models.Model):
    """
    A host for housing at a tournament.
    """
    address = models.CharField(
        help_text=_('The address of the host house.'),
        max_length=255,
        verbose_name=_('address'),
    )
    email = models.EmailField(
        blank=True,
        default='',
        help_text=_('An email address to contact the host.'),
        max_length=255,
        verbose_name=_('email'),
    )
    guests_max = models.PositiveSmallIntegerField(
        blank=True,
        help_text=_('The maximum number of guests that can be accomodated.'),
        null=True,
        verbose_name=_('Maximum Guest Count'),
    )
    guests_preferred = models.PositiveSmallIntegerField(
        help_text=_('The preferred number of guests to accomodate.'),
        verbose_name=_('Preferred Guest Count')
    )
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        verbose_name=_('ID'),
    )
    match = models.ForeignKey(
        'housing.HostTeamMatch',
        blank=True,
        help_text=_('The match object that the host is associated with.'),
        null=True,
        on_delete=models.SET_NULL,
        related_name='hosts',
        related_query_name='host',
        verbose_name=_('match'),
    )
    name = models.CharField(
        help_text=_('A name to identify the host.'),
        max_length=100,
        verbose_name=_('name'),
    )
    phone_number = models.CharField(
        blank=True,
        default='',
        help_text=_('A phone number to contact the host.'),
        max_length=30,
        verbose_name=_('phone number'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,         
        on_delete=models.CASCADE,
        help_text=_('The user who registered the host.'),
        related_name='hosts',
        related_query_name='host',

    )

    time_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('time created'),
    )
    tournament = models.ForeignKey(
        'housing.Tournament',
        help_text=_('The tournament to host for.'),
        on_delete=models.CASCADE,
        related_name='hosts',
        related_query_name='host',
    )

    class Meta:
        ordering = ('tournament__date_start', 'time_created')
        verbose_name = _('host')
        verbose_name_plural = _('hosts')

    def __str__(self):
        return self.name


class HostTeamMatch(models.Model):
    """
    A match between a team and multiple hosts.
    """
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        verbose_name=_('ID'),
    )
    team = models.OneToOneField(
        'housing.Team',
        help_text=_('The team that is matched with the hosts.'),
        on_delete=models.CASCADE,
    )
    time_created = models.DateTimeField(
        auto_now_add=True,
        help_text=_('The time the match was created.'),
        verbose_name=_('time created'),
    )

    class Meta:
        ordering = ('time_created',)
        verbose_name = _('host team match')
        verbose_name_plural = _('host team matches')

    def __str__(self):
        return f'Match for Team {self.team}'

    def get_absolute_url(self):
        return reverse(
            'housing:match-detail',
            kwargs={'slug': self.team.tournament.slug, 'slug_key': self.team.tournament.slug_key, 'uuid': self.id},
        )


class Team(models.Model):
    """
    A team attending a tournament.
    """
    arrival_time = models.DateTimeField(
        help_text=_('An estimated arrival time of the team.'),
        verbose_name=_('arrival time'),
    )
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        verbose_name=_('ID'),
    )
    name = models.CharField(
        help_text=_('The name of the team.'),
        max_length=255,
        verbose_name=_('name'),
    )
    player_count = models.PositiveSmallIntegerField(
        help_text=_('The number of team members who need housing.'),
        verbose_name=_('player count'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teams',
        related_query_name='team',
        help_text=_('The user who registered the Team.'),
    )

    time_created = models.DateTimeField(
        auto_now_add=True,
        help_text=_('The time the team registered.'),
        verbose_name=_('time created'),
    )
    tournament = models.ForeignKey(
        'housing.Tournament',
        help_text=_('The tournament the team is attending.'),
        on_delete=models.CASCADE,
        related_name='teams',
        related_query_name='team',
        verbose_name=_('tournament'),
    )

    class Meta:
        ordering = ('time_created',)
        verbose_name = _('team')
        verbose_name_plural = _('teams')

    def __str__(self):
        return self.name


class Tournament(models.Model):
    """
    A tournament occurs over a set time period in a location.
    """
    date_end = models.DateField(
        help_text=_('The end date of the tournament.'),
        verbose_name=_('end date'),
    )
    date_lockout = models.DateTimeField(
        help_text=_('The date and time to freeze host and team registrations '
                    'at. This may not be edited.'),
        verbose_name=_('registration lockout date'),
    )
    date_start = models.DateField(
        help_text=_('The start date of the tournament.'),
        verbose_name=_('start date'),
    )
    description = models.TextField(
        blank=True,
        default='',
        help_text=_('Additional information about the tournament.'),
    )
    location = models.CharField(
        help_text=_('The location where the tournament is occurring.'),
        max_length=255,
        verbose_name=_('location'),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('name'),
    )
    slug = models.SlugField(
        db_index=True,
        max_length=50,
        verbose_name=_('slug'),
    )
    slug_key = models.CharField(
        db_index=True,
        default=generate_slug_key,
        editable=False,
        help_text=_('A unique key to improve uniqueness of the slug.'),
        max_length=6,
        verbose_name=_('slug key'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        help_text=_('The user who registered the tournament.'),
        on_delete=models.CASCADE,
        related_name='tournaments',
        related_query_name='tournament',
        verbose_name=_('user'),
    )

    class Meta:
        ordering = ('date_start', 'name')
        verbose_name = _('tournament')
        verbose_name_plural = _('tournaments')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'housing:tournament-detail',
            kwargs={'slug': self.slug, 'slug_key': self.slug_key},
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:50]

        super().save(*args, **kwargs)
