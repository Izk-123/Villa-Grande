from django.urls import path
from lodge.views import custom_404
from . import views

app_name = 'accounts'

handler404 = custom_404

urlpatterns = [
    # Auth
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),

    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # User management
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    
    path('live-stats/', views.live_stats, name='live_stats'),
    path('user-update-role/', views.user_update_role, name='user_update_role'),
]