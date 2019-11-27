from django.urls import path
from bibliography import views


app_name = 'bibliography'
urlpatterns = [
    path('', views.bibliography_index_view, name='index'),
    path('full/', views.bibliography_full_view, name='full'),
    path('search/', views.bibliography_search_view, name='search'),
    path('reload/', views.bibliography_reload_view, name='reload'),
]
