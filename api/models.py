from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=30, unique=True)

    def __str__(self) -> str:
        return self.description


class Employee(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} from {self.team.name}"


class MoodLevel(models.Model):
    class Level(models.IntegerChoices):
        SAD = 1
        NORMAL = 2
        GOOD = 3
        BETTER = 4
        EXCELLENT = 5

    mood_level = models.IntegerField(choices=Level.choices)
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, unique_for_date="record_time"
    )
    record_time = models.DateField(default=datetime.utcnow)

    def __str__(self) -> str:
        return (
            f"{self.employee.username} was {self.get_mood_level_display()}"
            f" on {self.record_time.strftime('%A %d. %b %Y')}"
        )
