from django.urls import path, register_converter

from housing import converters, views


register_converter(converters.SlugKeyConverter, 'slug-key')


app_name = 'housing'

urlpatterns = [
    path(
        'tournaments/',
        views.TournamentListView.as_view(),
        name='tournament-list',
    ),
    path(
        'tournaments/<slug-key:slug_key>/<slug:slug>/',
        views.TournamentDetailView.as_view(),
        name='tournament-detail',
    ),
]
