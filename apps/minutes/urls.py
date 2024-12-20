from django.urls import path
from . import views
from .views import search_users
urlpatterns = [
    path('create/', views.submit_minutes, name='submit-minutes'),
    path('track/', views.track_minutes, name='track-minutes'),
    path('pending/', views.pending_minutes, name='pending-minutes'),
    path('approve/<int:minute_id>/', views.approve_minute, name='approve-minute'),
    path('api/search-users/', views.search_users, name='search-users'),


]

