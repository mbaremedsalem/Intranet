# Generated by Django 4.2.3 on 2023-12-21 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_avis_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avis',
            name='admin',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.admin'),
            preserve_default=False,
        ),
    ]
