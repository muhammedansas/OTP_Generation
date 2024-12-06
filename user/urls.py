from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home,name='home'),
    path('',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('otp_verification/',views.otp_verification,name='otp_verification'),
]
