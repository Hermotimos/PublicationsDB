from django.urls import path
from activity_log import views


app_name = 'activity_log'
urlpatterns = [
    path('', views.log_view, name='log'),
]
