from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="carting:geometry_first")),
    path("text", views.text_first, name="text_first"),
    path("geometry", views.geometry_first, name="geometry_first"),
    path(
        "proxy/wms",
        views.wms_proxy,
        kwargs={"wms_url": "https://services.data.shom.fr/INSPIRE/wms/v"},
        name="wms-proxy",
    ),
]
