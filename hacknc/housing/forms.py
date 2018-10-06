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
