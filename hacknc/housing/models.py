from django.conf import settings
from django.db import models
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


class Tournament(models.Model):
    """
    A tournament ocurrs over a set time period in a location.
    """
    date_end = models.DateField(
        help_text=_('The start date of the tournament.'),
        verbose_name=_('end date'),
    )
    date_start = models.DateField(
        help_text=_('The end date of the tournament.'),
        verbose_name=_('start date'),
    )
    description = models.TextField(
        blank=True,
        default='',
        help_text=_('Additional information about the tournament.'),
    )
    location = models.CharField(
        help_text=_('The location where the tournament is ocurring.'),
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:50]

        super().save(*args, **kwargs)
