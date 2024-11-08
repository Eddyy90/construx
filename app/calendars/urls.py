from django.urls import path, include
from . import views


app_name = 'calendars'
urlpatterns = [
    path('', views.EventListView.as_view(), name='list'),
    path('create/', views.EventCreateView.as_view(), name='create'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.EventUpdateView.as_view(), name='edit'),
    path('<int:pk>/remove/', views.EventDeleteView.as_view(), name='remove'),
    path('api/occurrences/', views.api_occurrences, name="api_occurrences"),
    path('api/move_or_resize/', views.api_move_or_resize_by_code, name="api_move_or_resize"),
    path('fullcalendar/', views.FullCalendarView.as_view(), name="fullcalendar"),
    path('ajax/detail/<int:pk>/', views.event_detail_modal, name='ajax_event_detail'),
    path('ajax/edit/<int:pk>/', views.event_edit_modal, name='ajax_event_edit'),

]
