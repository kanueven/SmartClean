from django.urls import path
from .views import (
    JobListCreateView,
    JobDetailView,
    GenerateQuoteView,
    AcceptQuoteView,
    CompleteJobView,
)

urlpatterns = [
    path("", JobListCreateView.as_view()),
    path("<int:pk>/", JobDetailView.as_view()),
    path("<int:pk>/generate-quote/", GenerateQuoteView.as_view()),
    path("<int:pk>/accept-quote/", AcceptQuoteView.as_view()),
    path("<int:pk>/complete/", CompleteJobView.as_view()),
]