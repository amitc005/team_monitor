from rest_framework.serializers import ModelSerializer

from api.models import MoodLevel


class MoodLevelSerializer(ModelSerializer):
    class Meta:
        model = MoodLevel
        fields = "__all__"
        read_only_fields = ["record_date"]
