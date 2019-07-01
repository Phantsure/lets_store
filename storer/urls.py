from django.urls import path

from . import views

app_name = 'storer'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('update/', views.update, name='update'),
    path('delete/<path:filename>', views.delete, name='delete'),
    path('download/<path:filename>', views.download, name='download'),
    path('files/', views.files, name='files'),
    path('details/<path:filename>', views.file_details, name='details'),
]