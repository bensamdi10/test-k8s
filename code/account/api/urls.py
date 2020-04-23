from django.conf.urls import url
from django.contrib import admin

from account.api import views

urlpatterns = [
    #### get list the components

    url(r'^active-theme/(?P<theme>.+)/$', views.ActiveTheme.as_view(), name="active_theme"),
    url(r'^active-layout/(?P<layout>.+)/$', views.ActiveLayout.as_view(), name="active_layout"),
    url(r'^disable-tour-backend/$', views.DisableTourBackend.as_view(), name="disable_tour_backend"),
    url(r'^disable-tour-site/$', views.DisableTourSite.as_view(), name="disable_tour_site"),

]



