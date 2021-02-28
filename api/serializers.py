from copy import deepcopy

from rest_framework.serializers import ModelSerializer

from api.models import Employee
from api.models import MoodLevel
from api.models import TeamStatistic
from api.utils import update_team_statistic


class MoodLevelSerializer(ModelSerializer):
    class Meta:
        model = MoodLevel
        fields = ["mood_level"]
        read_only_fields = ["record_date"]

    def create(self, validated_data):
        employee = Employee.objects.filter(user=self.context["request"].user).first()
        instance = MoodLevel.objects.filter(employee=employee).first()
        old_model = None
        if not instance:
            instance = MoodLevel(employee=employee)
        else:
            old_model = deepcopy(instance)

        instance.mood_level = validated_data["mood_level"]
        instance.save()
        update_team_statistic(employee.team, instance, old_model)
        return instance


class TeamStatisticSerializer(ModelSerializer):
    class Meta:
        model = TeamStatistic
        fields = "__all__"
