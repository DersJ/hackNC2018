# Generated by Django 2.1.2 on 2018-10-06 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('housing', '0002_host'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('arrival_time', models.DateTimeField(help_text='An estimated arrival time of the team.', verbose_name='arrival time')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the team.', max_length=255, verbose_name='name')),
                ('player_count', models.PositiveSmallIntegerField(help_text='The number of team members who need housing.', verbose_name='player count')),
                ('time_created', models.DateTimeField(auto_now_add=True, help_text='The time the team registered.', verbose_name='time created')),
                ('tournament', models.ForeignKey(help_text='The tournament the team is attending.', on_delete=django.db.models.deletion.CASCADE, related_name='teams', related_query_name='team', to='housing.Tournament', verbose_name='tournament')),
                ('user', models.ForeignKey(help_text='The user who registered the Team.', on_delete=django.db.models.deletion.CASCADE, related_name='teams', related_query_name='team', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'team',
                'verbose_name_plural': 'teams',
                'ordering': ('time_created',),
            },
        ),
    ]
