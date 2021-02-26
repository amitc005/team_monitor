from rest_framework.viewsets import generics

from api.models import MoodLevel
from api.serializers import MoodLevelSerializer


class MoodListView(generics.ListCreateAPIView):
    queryset = MoodLevel.objects.all()
    serializer_class = MoodLevelSerializer


class MoodView(generics.UpdateAPIView):
    queryset = MoodLevel.objects.all()
    serializer_class = MoodLevelSerializer
