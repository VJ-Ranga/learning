from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from academy import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('help/', views.setup_help, name='setup_help'),
    path('login/', views.QuestLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('join/', views.join, name='join'),
    path('missions/<slug:slug>/', views.mission_detail, name='mission'),
    path('api/missions/<slug:slug>/attempt/', views.attempt, name='attempt'),
    path('api/missions/<slug:slug>/solution/', views.solution, name='solution'),
    path('api/progress/', views.progress_api, name='progress'),
    path('downloads/terminal-programs.zip', views.downloads, name='downloads'),
    path('runner/', views.runner, name='runner'),
    path('admin/login/', views.QuestLoginView.as_view(), name='admin_login'),
    path('admin/', admin.site.urls),
]
