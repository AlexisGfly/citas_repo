from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('user/create_user', views.create_user),
    path('user/appointments', views.appointments),
    path('user/login', views.login),
    path('user/logout', views.logout),
    path('user/add_task', views.add_task),
    path('user/add_appointment', views.add_appointment),
    path('appointment/delete/<int:task_id>', views.delete_appointment)
]