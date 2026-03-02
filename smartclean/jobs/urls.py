from django.urls import path
from .views import (
    JobListCreateView,
    JobDetailView,
    GenerateQuoteView,
    AcceptQuoteView,
    CompleteJobView,
    CancelJobView,
    StartJobView
)

urlpatterns = [
    path("", JobListCreateView.as_view()),
    path("<int:pk>/", JobDetailView.as_view()),
    path('<int:pk>/generate-quote/', GenerateQuoteView.as_view(), name='job-generate-quote'),
    path('<int:pk>/accept-quote/', AcceptQuoteView.as_view(), name='job-accept-quote'),
    path('<int:pk>/start/',StartJobView.as_view(),name = "in-progress"),
    path('<int:pk>/complete/', CompleteJobView.as_view(), name='job-complete'),
    path('<int:pk>/cancel/', CancelJobView.as_view(), name='job-cancel'),
]