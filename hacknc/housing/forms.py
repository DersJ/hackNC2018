from django import forms

from housing import data_factory, models


class DummyDataForm(forms.Form):
    tournament_name = forms.CharField(
        help_text='The name of the tournament to create.',
        initial='Easterns',
    )

    def save(self, user, *args, **kwargs):
        tournament_name = self.cleaned_data['tournament_name']

        data_factory.create_dummy_data(user, tournament_name)


class TournamentForm(forms.ModelForm):
    """
    Form for creating and editing a tournament.
    """

    class Meta:
        fields = ('name', 'location', 'date_start', 'date_end', 'date_lockout', 'description')
        model = models.Tournament

    def clean(self):
        data = super().clean()

        if data['date_start'] > data['date_end']:
            self.add_error(
                'date_end',
                forms.ValidationError(
                    "The tournament's end date must be on or after its start "
                    "date."
                ),
            )

        if data['date_lockout'].date() > data['date_start']:
            self.add_error(
                'date_lockout',
                forms.ValidationError(
                    "The tournament's lockout date must be before the start "
                    "of the tournament.",
                ),
            )

        return data

    def save(self, user, *args, **kwargs):
        self.instance.user = user

        return super().save(*args, **kwargs)


class HostForm(forms.ModelForm):
    email = forms.EmailField(
        help_text='An email address for teams to contact the host at.',
    )
    phone_number = forms.CharField(
        help_text='A phone number for teams to contact the host at.',
        max_length=30,
    )

    class Meta:
        fields = (
            'name',
            'phone_number',
            'email',
            'address',
            'guests_preferred',
            'guests_max',
        )
        model = models.Host

    def __init__(self, tournament, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tournament = tournament

    def clean(self):
        data = super().clean()

        max_guests = data['guests_max']
        preferred_guests = data['guests_preferred']

        if max_guests is not None and max_guests < preferred_guests:
            self.add_error(
                'guests_max',
                forms.ValidationError(
                    "The maximum number of guests may not be lower than the "
                    "preferred number of guests.",
                ),
            )

        return data

    def save(self, user, *args, **kwargs):
        self.instance.tournament = self.tournament
        self.instance.user = user

        return super().save(*args, **kwargs)


class TeamForm(forms.ModelForm):
    arrival_time = forms.DateTimeField(help_text="Enter as YYYY-MM-DD HH:MM (24hr time).")
    class Meta:
        fields = ('arrival_time', 'name', 'player_count')
        model = models.Team
    def save(self, user, *args, **kwargs):
        self.instance.tournament = self.tournament
        self.instance.user= user
        return super().save(*args, **kwargs)
    def __init__(self, tournament, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tournament = tournament
