from django.conf.urls import url
from . import views

urlpatterns = [
    url("^$", views.index, name="index"),
    url("^forgot-api-key/$", views.forgot_api_key, name="forgot_api_key"),
    url("^documentation/$", views.documentation, name="documentation"),
    url("^get-api-key/$", views.get_api_key, name="get_api_key"),

    # API Routes
    url("^api/personal/$", views.personal_storage, name="personal_storage"),
]
