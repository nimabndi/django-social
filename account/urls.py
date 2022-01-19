from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('like/', views.post_like, name='post_like'),
    path('dislike/', views.post_dislike, name='post_dislike'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('dashboard/<int:user_id>/', views.user_dashboard, name='dashboard'),
    path('edit_profile/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path('phone_logine/', views.phone_login, name='phone_login'),
    path('verify/', views.verify, name='verify'),
    path('follow/', views.follow, name='follow'),
    path('unfollow/', views.unfollow, name='unfollow'),

    path('follower/<int:user_id>/', views.user_follower, name='user_follower'),
    path('following/<int:user_id>/', views.User_following, name='user_following'),
    path('change_password/<int:user_id>/', views.change_password, name='change_password'),


]
