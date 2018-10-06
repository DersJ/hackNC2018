from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from housing import models


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
