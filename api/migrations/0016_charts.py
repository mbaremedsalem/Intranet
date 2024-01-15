# Generated by Django 4.2.3 on 2024-01-01 12:27

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='charts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200, null=True)),
                ('description', models.CharField(max_length=400, null=True)),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('file', models.FileField(null=True, upload_to=api.models.uoload_document)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.admin')),
                ('user', models.ManyToManyField(related_name='chartes_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
