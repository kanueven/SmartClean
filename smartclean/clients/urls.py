from django.urls import path
from .views import ClientListCreateView, ClientRetrieveUpdateDestroyView

urlpatterns = [
    path('clients/', ClientListCreateView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientRetrieveUpdateDestroyView.as_view(), name='client-detail'),
]