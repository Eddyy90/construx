from django.urls import path

from . import views

app_name = 'groups'
urlpatterns = [
    path('', views.GroupListView.as_view(), name='index'),
    path('create/', views.GroupCreateView.as_view(), name='create'),
    path('<int:pk>/', views.GroupDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.GroupUpdateView.as_view(), name='edit'),
    path('<int:pk>/remove/', views.GroupDeleteView.as_view(), name='remove'),
]
