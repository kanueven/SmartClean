from django.urls import path
from .views import ServiceListCreateView, ServiceUpdateView

urlpatterns = [
    path("", ServiceListCreateView.as_view()),
    path("<int:pk>/", ServiceUpdateView.as_view()),
]