from django.urls import path
from rest_framework.authtoken import views
from rest_framework.views import APIView

urlpatterns = [
    path('token/', views.obtain_auth_token),
    path('call-event/', APIView.as_view(), name='call-event'),
]
