from django.urls import path

from . import views

app_name = 'storer'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
    path('download/file.txt', views.download, name='download'),
]