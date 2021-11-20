from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomePage.as_view(),name = 'HomePage'),
    path('login',views.LoginUser.as_view(),name = 'LoginUser'),
    path('signup',views.SignupUser.as_view(),name = 'SignupUser'),
    path('logout',views.LogoutUser.as_view(),name = 'LogoutUser')
]