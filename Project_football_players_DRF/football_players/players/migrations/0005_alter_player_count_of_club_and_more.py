# Generated by Django 4.2.7 on 2023-11-27 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0004_alter_player_count_of_club_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='count_of_club',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='player',
            name='football_player_name',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='player',
            name='nationality',
            field=models.CharField(max_length=60),
        ),
    ]
