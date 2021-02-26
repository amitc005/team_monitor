from django.urls import path

from api.views import MoodListView
from api.views import MoodView

urlpatterns = [
    path("moods", MoodListView.as_view()),
    path(r"moods/<pk>", MoodView.as_view()),
]
