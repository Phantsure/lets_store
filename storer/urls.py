from django.urls import path

from . import views

app_name = 'storer'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('update/', views.update, name='update'),
    path('delete/<str:filename>', views.delete, name='delete'),
    path('download/<str:filename>', views.download, name='download'),
    path('files/', views.files, name='files'),
    path('details/<str:filename>', views.file_details, name='details'),
]