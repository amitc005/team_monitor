from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Level(models.IntegerChoices):
    SAD = 1
    NORMAL = 2
    GOOD = 3
    BETTER = 4
    EXCELLENT = 5


class Team(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=30, unique=True)
    avg_mood = models.IntegerField(default=1, choices=Level.choices)
    total_sad = models.IntegerField(default=0)
    total_average = models.IntegerField(default=0)
    total_good = models.IntegerField(default=0)
    total_better = models.IntegerField(default=0)
    total_excellent = models.IntegerField(default=0)

    def increment_total_mood_level(self, mood_level):
        if mood_level == 1:
            self.total_sad += 1
        if mood_level == 2:
            self.total_average += 1
        if mood_level == 3:
            self.total_good += 1
        if mood_level == 4:
            self.total_better += 1
        if mood_level == 5:
            self.total_excellent += 1

    def __str__(self):
        return self.description


class Employee(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    current_mood_level = models.IntegerField(default=1, choices=Level.choices)

    def __str__(self):
        return f"{self.name} from {self.team.name}"


class MoodLevel(models.Model):
    class Meta:
        unique_together = [["employee", "record_date"]]

    mood_level = models.IntegerField(choices=Level.choices)
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, unique_for_date="record_date"
    )
    record_date = models.DateField(blank=False, auto_now_add=True)

    def __str__(self):
        return (
            f"{self.employee.name} was {self.get_mood_level_display()}"
            f" on {self.record_date.strftime('%A %d. %b %Y')}"
        )
