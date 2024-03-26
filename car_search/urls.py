from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'car_search'  # Define app namespace

urlpatterns = [
    path('', views.index, name='index'),     # Home page
    path('search/', views.search, name='search'),  # Search page
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




