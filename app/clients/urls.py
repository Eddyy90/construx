from django.urls import path

from . import views

app_name = 'clients'
urlpatterns = [
    path('', views.ClientsView.as_view(), name='index'),
    path('<int:pk>/', views.client_detail, name='detail'),
    path('profile/<int:pk>/edit', views.root_edit_settings, name='edit_profile'),
    # path('<int:pk>/update/', views.OccupationAreaUpdateView.as_view(), name='edit'),
    # path('<int:pk>/remove/', views.OccupationAreaDeleteView.as_view(), name='remove'),
    # path('<int:client_id>/delete/', views.delete, name='delete'),
]
