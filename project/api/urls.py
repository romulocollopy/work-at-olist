from django.urls import path
from rest_framework.authtoken import views as rf_views
from . import views as api_views

urlpatterns = [
    path('token/', rf_views.obtain_auth_token),
    path('call-event/', api_views.CallEventView.as_view(), name='call-event'),
    path('call-bill/', api_views.CallBillView.as_view(), name='call-bill'),
]
