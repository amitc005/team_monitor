# Generated by Django 3.1.7 on 2021-02-26 05:43
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("api", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="current_mood_level",
            field=models.IntegerField(default=1),
        )
    ]
