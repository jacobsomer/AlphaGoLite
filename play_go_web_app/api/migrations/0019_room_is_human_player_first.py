# Generated by Django 3.2.3 on 2021-06-01 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_alter_room_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='is_human_player_first',
            field=models.BooleanField(default=False),
        ),
    ]
