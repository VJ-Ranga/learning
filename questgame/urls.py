from django.contrib import admin
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path
from academy import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('help/', views.setup_help, name='setup_help'),
    path('login/', views.QuestLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/change/', PasswordChangeView.as_view(template_name='registration/password_change.html', success_url='/password/changed/'), name='password_change'),
    path('password/changed/', PasswordChangeDoneView.as_view(template_name='registration/password_changed.html'), name='password_change_done'),
    path('missions/<slug:slug>/', views.mission_detail, name='mission'),
    path('api/missions/<slug:slug>/attempt/', views.attempt, name='attempt'),
    path('api/missions/<slug:slug>/solution/', views.solution, name='solution'),
    path('api/progress/', views.progress_api, name='progress'),
    path('downloads/terminal-programs.zip', views.downloads, name='downloads'),
    path('runner/', views.runner, name='runner'),
    path('admin/login/', views.QuestLoginView.as_view(), name='admin_login'),
    path('admin/', admin.site.urls),
]
