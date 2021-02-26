from django.contrib import admin

from api.models import Employee
from api.models import MoodLevel
from api.models import Team

# Register your models here.

admin.site.register(Team)
admin.site.register(Employee)
admin.site.register(MoodLevel)
