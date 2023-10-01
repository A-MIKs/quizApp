from django.urls import path
from .views import *

app_name = "quizes"

urlpatterns = [
    path("", QuizListView.as_view(), name="main-view"),
    path("<int:pk>/", quiz_view, name="quiz-view"),
    path("<pk>/data/", quiz_data_view, name="quiz-data-view"),
    path("<int:pk>/save/", save_quiz_view, name="quiz-view"),

]