from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import generic

from housing import models


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
