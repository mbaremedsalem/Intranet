# Generated by Django 4.2.3 on 2023-12-19 16:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_avis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='avis',
            name='user',
        ),
        migrations.AddField(
            model_name='avis',
            name='users',
            field=models.ManyToManyField(related_name='avis_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
