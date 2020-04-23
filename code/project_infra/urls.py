"""project_infra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from . import views
import django.views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/backend/', include(('backend.api.urls', 'backend'), namespace='backend_api')),
    path('account/', include(('account.urls', 'account'), namespace='account')),

    path('', views.Home.as_view()),
    path('workspace/<str:project>/<str:env>/', views.Workspace.as_view()),

    path('run-env/<str:env>/', views.RunEnv.as_view()),
    path('connect-cli/', views.ConnectCli.as_view()),


]
