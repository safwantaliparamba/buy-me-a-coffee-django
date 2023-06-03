from django.urls import re_path

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from api.v1.accounts import views


urlpatterns = [
    re_path(r'^register/$', views.register),
    re_path(r'^login/$', views.login),

    re_path(r'^pay/$', views.pay),
    re_path(r'^pay/verification/$', views.payment_verification),

    re_path(r'^token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
]
