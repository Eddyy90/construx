from django.urls import path
from .import views


urlpatterns = [
    path('', views.login, name="index"),
    #path('', views.index, name="index" ),
    path('dashboard', views.index,name="dashboard"),
    path('wizard', views.wizard, name="wizard"),
    path('profile', views.profile_detail, name="profile_detail"),
    path('profile/edit', views.edit_profile, name="profile_edit"),
    path('profile/impersonate', views.impersonate_profile, name="profile_impersonate"),
    path('profile/unimpersonate', views.unimpersonate_profile, name="profile_unimpersonate"),
    path('support', views.support, name="support"),
]
