from django import forms

from housing import models


class TournamentForm(forms.ModelForm):
    """
    Form for creating and editing a tournament.
    """

    class Meta:
        fields = ('name', 'location', 'date_start', 'date_end', 'description')
        model = models.Tournament

    def save(self, user, *args, **kwargs):
        self.instance.user = user

        return super().save(*args, **kwargs)


class HostForm(forms.ModelForm):
	class Meta:
		fields = ('name', 'phone_number', 'email', 'address', 'guests_max', 'guests_preferred')
		model = models.Host
	def save(self, *args, **kwargs):
		self.instance.tournament = self.tournament
		return super().save(*args, **kwargs)
	def __init__(self, tournament, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.tournament = tournament


class TeamForm(forms.ModelForm):
	class Meta:
		fields = ('arrival_time', 'name', 'player_count')
		model = models.Team
	def save(self, *args, **kwargs):
		self.instance.tournament = self.tournament
		return super().save(*args, **kwargs)
	def __init__(self, tournament, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.tournament = tournament