from django.urls import path
from bibliography import views


app_name = 'bibliography'
urlpatterns = [
    path('', views.bibliography_main_view, name='bibliography-main'),
]
