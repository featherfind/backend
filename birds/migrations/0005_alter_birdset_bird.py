# Generated by Django 5.1.4 on 2025-01-04 03:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0004_alter_birdset_audio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birdset',
            name='bird',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='birdsets', to='birds.bird'),
        ),
    ]
