from django.urls import path
from .views import RegisterView, ListUsersView,UserDetailView
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name= 'token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', ListUsersView.as_view(), name='list-users'),
    path('users/<int:pk>/',UserDetailView.as_view(),name = 'user-detail')
]
