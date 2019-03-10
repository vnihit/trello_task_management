from django.conf.urls import url

from . import views

urlpatterns = [
    url("local/", views.LocalAuth.as_view()),
    url("test/", views.test)
]