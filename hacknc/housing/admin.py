from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from housing import models


@admin.register(models.Host)
class HostAdmin(admin.ModelAdmin):
    autocomplete_fields = ('tournament',)
    fieldsets = (
        (
            None,
            {
                'fields': ('tournament',),
            },
        ),
        (
            _('Accomodation Information'),
            {
                'fields': ('address', 'guests_preferred', 'guests_max'),
            },
        ),
        (
            _('Contact Information'),
            {
                'fields': ('name', 'email', 'phone_number'),
            },
        ),
        (

            _('Time Information'),
            {
                'classes': ('collapse',),
                'fields': ('time_created',),
            },
        ),
    )
    list_display = ('name', 'tournament', 'guests_preferred', 'guests_max')
    readonly_fields = ('time_created',)
    search_fields = ('email', 'name', 'tournament__name')


@admin.register(models.Tournament)
class TournamentAdmin(admin.ModelAdmin):
    autocomplete_fields = ('user',)
    date_hierarchy = 'date_start'
    fieldsets = (
        (
            None,
            {
                'fields': ('name', 'user'),
            },
        ),
        (
            _('Location'),
            {
                'fields': ('location',),
            },
        ),
        (
            _('Date'),
            {
                'fields': ('date_start', 'date_end'),
            },
        ),
        (
            _('Additional Information'),
            {
                'fields': ('description',),
            },
        ),
        (
            _('Slugs'),
            {
                'classes': ('collapse',),
                'fields': ('slug', 'slug_key'),
            },
        ),
    )
    list_display = ('name', 'date_start', 'date_end')
    readonly_fields = ('slug', 'slug_key')
    search_fields = ('location', 'name')
