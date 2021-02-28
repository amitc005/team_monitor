from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import generics

from api.models import Employee
from api.models import MoodLevel
from api.models import TeamStatistic
from api.serializers import MoodLevelSerializer
from api.serializers import TeamStatisticSerializer


class MoodListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MoodLevel.objects.all()
    serializer_class = MoodLevelSerializer


class TeamStaticsList(generics.ListAPIView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return TeamStatistic.objects.all()

        employee = Employee.objects.filter(user=self.request.user).first()
        return TeamStatistic.objects.filter(team=employee.team)

    serializer_class = TeamStatisticSerializer
