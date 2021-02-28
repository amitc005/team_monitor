from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg
from django.db.models import Q

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

    def __str__(self):
        return self.description


class TeamStatistic(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    avg_mood = models.IntegerField(default=1, choices=Level.choices)
    total_sad = models.IntegerField(default=0)
    total_normal = models.IntegerField(default=0)
    total_good = models.IntegerField(default=0)
    total_better = models.IntegerField(default=0)
    total_excellent = models.IntegerField(default=0)

    def update_stats(self, mood_level, previous_level):
        total_field_dict = {
            1: "total_sad",
            2: "total_normal",
            3: "total_good",
            4: "total_better",
            5: "total_excellent",
        }

        if previous_level in total_field_dict:
            old_total = getattr(self, total_field_dict[previous_level])
            setattr(self, total_field_dict[mood_level.mood_level], old_total - 1)

        if mood_level.mood_level in total_field_dict:
            old_total = getattr(self, total_field_dict[mood_level.mood_level])
            setattr(self, total_field_dict[mood_level.mood_level], old_total + 1)

        avg_mood = MoodLevel.objects.filter(Q(employee__team=self.team)).aggregate(
            Avg("mood_level")
        )
        self.avg_mood = avg_mood["mood_level__avg"]


class Employee(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class MoodLevel(models.Model):
    class Meta:
        unique_together = [["employee", "record_date"]]

    mood_level = models.IntegerField(choices=Level.choices)
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, unique_for_date="record_date"
    )
    record_date = models.DateField(blank=False, auto_now_add=True)

    def __str__(self):
        return f"{self.employee.name} on {self.record_date.strftime('%A %d. %b %Y')}"
