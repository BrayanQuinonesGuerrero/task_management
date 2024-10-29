from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]