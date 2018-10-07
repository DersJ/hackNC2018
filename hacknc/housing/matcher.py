"""
Responsible for matching teams with hosts.
"""

from django.db.models import F, Sum
from django.db.models.functions import Coalesce

from housing import models


def find_hosts(team, hosts, guest_attr):
    """
    Produce an array of the best hosts for a given team.

    Args:
        team:
            The team to find hosts for.
        hosts:
            The possible list of hosts.
        guest_attr:
            The attribute of the host model identifying the number of
            guests that can be accomodated.

    Returns:
        An array of the hosts to assign to the team. If the team cannot
        be accomodated, ``None`` is returned.
    """
    players = team.player_count
    chosen_hosts = []

    # We create a copy so we can remove elements without affecting the
    # main host list. If we don't end up satisfying the team's
    # requirements, we can avoid affecting the main list since we only
    # mutated the copy.
    hosts_copy = [host for host in hosts]

    while players > 0:
        if not hosts_copy:
            return None

        chosen_host = None
        for host in hosts_copy:
            chosen_host = host
            if getattr(host, guest_attr) >= players:
                break

        hosts_copy.remove(host)
        chosen_hosts.append(chosen_host)
        players -= getattr(chosen_host, guest_attr)

    # If we've satisfied the requirements for a team, we remove the
    # chosen hosts from the main list.
    for host in chosen_hosts:
        hosts.remove(host)

    return chosen_hosts


def get_guest_totals(tournament):
    """
    Get preferred and maximum guest counts.
    """
    counts = models.Host.objects.filter(
        tournament=tournament,
    ).annotate(
        guests_max_default=Coalesce(F('guests_max'), F('guests_preferred')),
    ).aggregate(
        max_guest_count=Sum('guests_max_default'),
        preferred_guest_count=Sum('guests_preferred'),
    )

    return {
        'guests_max_default': counts['max_guest_count'],
        'guests_preferred': counts['preferred_guest_count'],
    }


def match_teams(tournament):
    guest_counts = get_guest_totals(tournament)

    possible_matches_arr = []
    for guest_attr in ('guests_max_default', 'guests_preferred'):
        hosts = models.Host.objects.filter(
            match=None,
            tournament=tournament,
        )
        hosts = hosts.annotate(
            guests_max_default=Coalesce(
                F('guests_max'), F('guests_preferred'),
            ),
        )
        hosts = hosts.order_by(f'{guest_attr}')

        # If there are no hosts for the tournament, we bail
        if not hosts.exists():
            break

        host_list = list(hosts)

        possible_matches = []
        for team in tournament.teams.all():
            if team.player_count > guest_counts[guest_attr]:
                continue

            team_hosts = find_hosts(team, host_list, guest_attr)
            if team_hosts is not None:
                match = models.HostTeamMatch(team=team)
                match.hosts_temp = team_hosts
                possible_matches.append(match)

                guest_counts[guest_attr] -= team.player_count

        possible_matches_arr.append(possible_matches)

    if possible_matches_arr:
        max_matches = max(possible_matches_arr, key=len)

        for match in max_matches:
            match.save()
            for host in match.hosts_temp:
                host.match = match
                host.save()

    tournament.is_matched = True
    tournament.save()
