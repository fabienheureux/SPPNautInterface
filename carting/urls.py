from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("proxy/wms", views.wms_proxy, name="wms-proxy"),
]
