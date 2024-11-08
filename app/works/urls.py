from django.urls import path
from . import views


app_name = 'works'
urlpatterns = [
    path('', views.WorkListView.as_view(), name='list'),
    path('create/', views.WorkCreateView.as_view(), name='create'),
    path('<int:pk>/', views.WorkDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.WorkUpdateView.as_view(), name='edit'),
    path('<int:pk>/remove/', views.WorkDeleteView.as_view(), name='remove'),
]
