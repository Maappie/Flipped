from django.urls import path
from . import views 

urlpatterns = [
    # The API endpoint (Hidden logic)
    path('auth/google/', views.GoogleLoginView.as_view(), name='google-login'),
    
    path('login/', views.login_page, name='login-page'),
    path('profile/', views.profile_view, name='profile'),
    path('logout', views.logout_view, name='logout'),
]