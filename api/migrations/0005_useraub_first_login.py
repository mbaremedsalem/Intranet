# Generated by Django 4.2.3 on 2024-05-06 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_avis_file_alter_charts_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraub',
            name='first_login',
            field=models.BooleanField(default=True),
        ),
    ]
