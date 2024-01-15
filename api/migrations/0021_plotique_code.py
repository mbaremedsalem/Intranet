# Generated by Django 4.2.3 on 2024-01-15 13:01

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_alter_note_code_decision'),
    ]

    operations = [
        migrations.AddField(
            model_name='plotique',
            name='code',
            field=models.CharField(default=api.models.generate_unique_plotique_code, editable=False, max_length=100, null=True),
        ),
    ]
