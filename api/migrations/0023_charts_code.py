# Generated by Django 4.2.3 on 2024-04-16 22:14

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_alter_useraub_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='charts',
            name='code',
            field=models.CharField(default=api.models.generate_unique_decision_code, editable=False, max_length=100, null=True),
        ),
    ]
