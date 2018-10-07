from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import generic, View
from .matcher import match_teams
from housing import forms, models


class TournamentCreateView(LoginRequiredMixin, generic.FormView):
    """
    Create a new tournament.
    """
    form_class = forms.TournamentForm
    template_name = 'housing/tournament-create.html'

    def form_valid(self, form):
        tournament = form.save(user=self.request.user)

        return redirect(tournament.get_absolute_url())


class TournamentListView(generic.ListView):
    template_name = 'housing/tournament-list.html'

    def get_queryset(self):
        return models.Tournament.objects.filter(
            date_end__gte=timezone.now(),
        )


class TournamentDetailView(generic.DetailView):
    """
    View the details of a specific tournament.
    """
    context_object_name = 'tournament'
    template_name = 'housing/tournament-detail.html'

    def get_object(self):
        """
        Get the tournament instance whose parameters are specified in
        the URL.

        Returns:
            The tournament instance with the given slug and slug key.
        """
        return get_object_or_404(
            models.Tournament,
            slug=self.kwargs.get('slug'),
            slug_key=self.kwargs.get('slug_key'),
        )

class HostCreateView(LoginRequiredMixin, generic.FormView):
    form_class= forms.HostForm
    template_name = 'housing/host-create.html'
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tournament'] = get_object_or_404(
            models.Tournament,
            slug=self.kwargs.get('slug'),
            slug_key=self.kwargs.get('slug_key'),
        )
        return kwargs

    def form_valid(self, form):
        host = form.save(self.request.user)
        messages.success(
            self.request,
            f'Registered {host.name} as a host for {form.tournament}.',
        )

        return redirect(form.tournament.get_absolute_url())


class TeamCreateView(LoginRequiredMixin, generic.FormView):
    form_class= forms.TeamForm
    template_name = 'housing/team-create.html'
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tournament'] = get_object_or_404(
            models.Tournament,
            slug=self.kwargs.get('slug'),
            slug_key=self.kwargs.get('slug_key'),
        )
        return kwargs

    def form_valid(self, form):
        team = form.save(self.request.user)
        messages.success(
            self.request,
            f'Registered {team} as a team for {team.tournament}',
        )

        return redirect(form.tournament.get_absolute_url())

class MatchDetailView(LoginRequiredMixin, generic.DetailView):

    context_object_name = 'match'
    template_name = 'housing/match-detail.html'

    def get_object(self):
        """
        Get the tournament instance whose parameters are specified in
        the URL.

        Returns:
            The tournament instance with the given slug and slug key.
        """
        return get_object_or_404(
            models.HostTeamMatch,
            id=self.kwargs.get('uuid'),
        )

class MatcherView(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        tournament = get_object_or_404(
            models.Tournament,
            slug=kwargs.get('slug'),
            slug_key=kwargs.get('slug_key'),
        )
        match_teams(tournament)

        messages.success(
            request,
            f'Generated matches for {tournament}',
        )

        return redirect('profile')


