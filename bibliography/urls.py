from django.urls import path
from bibliography import views


app_name = 'bibliography'
urlpatterns = [
    path('', views.bibliography_main_view, name='main'),
    path('full/', views.bibliography_full_view, name='full'),
    path('index/', views.bibliography_index_view, name='index'),
    path('search/', views.bibliography_search_view, name='search'),
    path('search-results/', views.bibliography_search_results_view, name='search-results'),
]
