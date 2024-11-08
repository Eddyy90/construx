from django.urls import path
from . import views


app_name = 'user_notifications'
urlpatterns = [
    path('', views.NotificationListView.as_view(), name='list'),
    path('timeline/', views.NotificationTimelineView.as_view(), name='timeline'),
    path('create/', views.NotificationCreateView.as_view(), name='create'),
    path('<int:pk>/', views.NotificationDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.NotificationUpdateView.as_view(), name='edit'),
    path('<int:pk>/remove/', views.NotificationDeleteView.as_view(), name='remove'),
]
