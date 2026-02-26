from django.urls import path
from .views import CleanerListCreateView, CleanerRetrieveUpdateDestroyView

urlpatterns = [
    path('cleaners/', CleanerListCreateView.as_view(), name='cleaner-list-create'),
    path('cleaners/<int:pk>/', CleanerRetrieveUpdateDestroyView.as_view(), name='cleaner-detail'),
]