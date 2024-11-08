from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/edit', views.edit, name='edit'),
    # path('<int:client_id>/delete/', views.delete, name='delete'),
]
