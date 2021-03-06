# Generated by Django 2.1.2 on 2018-10-06 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('housing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('address', models.CharField(help_text='The address of the host house.', max_length=255, verbose_name='address')),
                ('email', models.EmailField(blank=True, default='', help_text='An email address to contact the host.', max_length=255, verbose_name='email')),
                ('guests_max', models.PositiveSmallIntegerField(blank=True, help_text='The maximum number of guests that can be accomodated.', null=True, verbose_name='Maximum Guest Count')),
                ('guests_preferred', models.PositiveSmallIntegerField(help_text='The preferred number of guests to accomodate.', verbose_name='Preferred Guest Count')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(help_text='A name to identify the host.', max_length=100, verbose_name='name')),
                ('phone_number', models.CharField(blank=True, default='', help_text='A phone number to contact the host.', max_length=30, verbose_name='phone number')),
                ('time_created', models.DateTimeField(auto_now_add=True, verbose_name='time created')),
                ('tournament', models.ForeignKey(help_text='The tournament to host for.', on_delete=django.db.models.deletion.CASCADE, related_name='hosts', related_query_name='host', to='housing.Tournament')),
                ('user', models.ForeignKey(help_text='The user who registered the host.', on_delete=django.db.models.deletion.CASCADE, related_name='hosts', related_query_name='host', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'host',
                'verbose_name_plural': 'hosts',
                'ordering': ('tournament__date_start', 'time_created'),
            },
        ),
    ]
