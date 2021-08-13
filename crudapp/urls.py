from django.urls import path 
from . import views

urlpatterns = [
    path('', views.add_show, name='home'),
    path('delete-record/<int:id>', views.delete_record, name="delete-record"),
    path('update-record/<int:id>', views.update_record, name='update-record'),
    path('update-database', views.update_database, name="update-database"),
    path('download-record', views.delete_record, name="download-record"),
]