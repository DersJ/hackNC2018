import pytest

from housing import matcher, models


# Test cases are each an array containing three rows:
# 1. An array of team sizes.
# 2. An array of host sizes.
# 3. An array where each element corresponds to the matches for the team
#    with the same index. If the element is 'None', no matches should
#    have been created for the team.


TEST_CASES = [
    [
        # Create one team with 17 players
        [17],
        # Create three hosts with 12, 3, and 1 spots, respectively
        [12, 3, 1],
        # The first team should have no matches
        [None],
    ],
    [
        [17, 14],
        [12, 3, 1],
        # First team has no matches, second matched with hosts at
        # indices 0 and 1.
        [None, [0, 1]],
    ],
    [
        [23, 23, 17],
        [20, 18, 14],
        [[0, 2], None, [1]],
    ],
    [
        [8, 18, 14],
        [17, 13, 7, 6, 2],
        [[1], [0, 4], None],
    ],
    [
        [3, 4, 5],
        [6, 4, 2, 2],
        [[1], [0], None],
    ]
]


@pytest.mark.parametrize('team_sizes,host_sizes,matches', TEST_CASES)
def test_match_teams(
        host_factory,
        host_sizes,
        matches,
        team_factory,
        team_sizes,
        tournament_factory):
    """
    Test various matching configurations.
    """
    tournament = tournament_factory()

    teams = []
    for i, team_size in enumerate(team_sizes):
        teams.append(
            team_factory(
                name=f'Team {i + 1}',
                player_count=team_size,
                tournament=tournament,
            ),
        )

    hosts = []
    for i, host_size in enumerate(host_sizes):
        hosts.append(
            host_factory(
                name=f'Host {chr(65 + i)}',
                guests_preferred=host_size,
                tournament=tournament,
            ),
        )

    matcher.match_teams(tournament)

    for team in teams:
        team.refresh_from_db()

    for host in hosts:
        host.refresh_from_db()

    for team, match in zip(teams, matches):
        if match is None:
            assert not hasattr(team, 'hostteammatch')
        else:
            for host_index in match:
                assert hosts[host_index].match == team.hostteammatch
