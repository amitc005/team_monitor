# Generated by Django 3.1.7 on 2021-02-26 07:07
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("api", "0004_auto_20210226_0700")]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="current_mood_level",
            field=models.IntegerField(
                choices=[
                    (1, "Sad"),
                    (2, "Normal"),
                    (3, "Good"),
                    (4, "Better"),
                    (5, "Excellent"),
                ],
                default=1,
            ),
        ),
        migrations.AlterField(
            model_name="team",
            name="avg_mood",
            field=models.IntegerField(
                choices=[
                    (1, "Sad"),
                    (2, "Normal"),
                    (3, "Good"),
                    (4, "Better"),
                    (5, "Excellent"),
                ],
                default=1,
            ),
        ),
    ]
