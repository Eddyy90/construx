from django.urls import path
from . import views


app_name = 'animals'
urlpatterns = [
    path('', views.AnimalListView.as_view(), name='list'),
    path('create/', views.AnimalCreateView.as_view(), name='create'),
    path('<int:pk>/', views.AnimalDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.AnimalUpdateView.as_view(), name='edit'),
    path('<int:pk>/remove/', views.AnimalDeleteView.as_view(), name='remove'),
]
