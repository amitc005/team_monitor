from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import MoodListView
from api.views import TeamStaticsList


urlpatterns = [
    path("mood_levels", MoodListView.as_view()),
    path("team_stats", TeamStaticsList.as_view()),
    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
