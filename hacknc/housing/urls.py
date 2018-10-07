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
        'tournaments/create/',
        views.TournamentCreateView.as_view(),
        name='tournament-create',
    ),
    path(
        'tournaments/<slug-key:slug_key>/<slug:slug>/',
        views.TournamentDetailView.as_view(),
        name='tournament-detail',
    ),
    path(
        'tournaments/<slug-key:slug_key>/<slug:slug>/addhost/', 
        views.HostCreateView.as_view(), 
        name='host-create',
    ),
    path(
        'tournaments/<slug-key:slug_key>/<slug:slug>/addteam/', 
        views.TeamCreateView.as_view(), 
        name='team-create',
    ),
    path(
        'tournaments/<slug-key:slug_key>/<slug:slug>/match/<uuid:uuid>/',
        views.MatchDetailView.as_view(),
        name='match-detail',
        ),
    path('tournaments/<slug-key:slug_key>/<slug:slug>/matcher/',
        views.MatcherView.as_view(),
        name='matcher'),
]
