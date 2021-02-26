from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import MoodLevel


@receiver(post_save, sender=MoodLevel)
def update_average_happiness(sender, instance, **kwargs):
    instance.employee.current_mood_level = instance.mood_level
    instance.employee.save()

    team = instance.employee.team
    avg_mood = team.employee_set.all().aggregate(Avg("current_mood_level"))
    team.avg_mood = avg_mood["current_mood_level__avg"]
    team.avg_mood = avg_mood["current_mood_level__avg"]
    team.increment_total_mood_level(instance.mood_level)
    instance.employee.team.save()
