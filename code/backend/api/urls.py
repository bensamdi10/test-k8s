from django.conf.urls import url
from django.contrib import admin

from backend.api import views
from django.urls import path

urlpatterns = [
    #### get list the components

    path('save-element/<str:element>/', views.SaveElement.as_view(), name='save-element'),
    path('get-element/<str:element>/<str:uid>/', views.GetElement.as_view(), name='get-element'),
    path('get-containers/<str:env>/', views.GetContainers.as_view(), name='get-containers'),
    path('get-volumes/<str:env>/', views.GetVolumes.as_view(), name='get-volumes'),
    path('get-clusters/<str:env>/', views.GetClusters.as_view(), name='get-clusters'),
    path('get-env-variables/<str:env>/', views.GetEnvVariables.as_view(), name='get-env-variables'),
    path('get-templates/<str:element>/', views.GetTemplates.as_view(), name='get-templates'),
    path('update-element/<str:element>/<str:uid>/', views.UpdateElement.as_view()),
    path('update-inline-element/<str:element>/<str:uid>/', views.UpdateInlineElement.as_view()),
    path('delete-element/<str:element>/<str:uid>/', views.DeleteElement.as_view()),
    path('archive-element/<str:type>/<str:uid>/', views.ArchiveElement.as_view()),
    path('archive-items/<str:type>/', views.ArchiveItems.as_view()),
    path('generate-yaml/<str:env>/', views.GenerateYaml.as_view()),
    path('generate-yaml-cli/<str:env>/', views.GenerateYamlCLI.as_view()),
    path('get-cli-credits/<str:token>/<str:name_space>/', views.GetCLICredits.as_view()),

    path('run-env/<str:env>/', views.RunEnv.as_view()),


]


'''

'''
