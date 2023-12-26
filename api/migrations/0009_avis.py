# Generated by Django 4.2.3 on 2023-12-19 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_useraub_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200, null=True)),
                ('description', models.CharField(max_length=500, null=True)),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='avis_admin', to='api.admin')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='avis_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]