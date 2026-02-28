from django.urls import path
from .views import ServiceListCreateView, ServiceRetrieveUpdateDestroyView,JobServiceListCreateView,JobServiceDestroyView

urlpatterns = [
    path("", ServiceListCreateView.as_view()),
    path("<int:pk>/", ServiceRetrieveUpdateDestroyView.as_view()),
    path('job/<int:job_id>/', JobServiceListCreateView.as_view(), name='job-service-list'),
    path('job/<int:job_id>/<int:pk>/', JobServiceDestroyView.as_view(), name='job-service-delete')
    
]