from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^base1$', views.base1),
    url(r'^presentation$', views.presentation),
    url(r'^contact$', views.contact),
    url(r'^recommandation$', views.recommandation),
]
