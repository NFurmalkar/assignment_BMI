from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.regi,name="regi"),
    path('login/', views.loginUser,name="loginUser"),
    path('logout/', views.logoutUser,name="logoutUser"),
    path('register/', views.register,name="register"),
    path('get-OTP/', views.getOTP,name="getOTP"),
    path('home/', views.home,name="home"),
    path('addBMI/', views.addBMI,name="addBMI"),
    path('updateBMI/<int:id>/', views.updateBMI,name="updateBMI"),
    path('deleteBMI/<int:id>/', views.deleteBMI,name="deleteBMI"),

    path('forgetPassword/', views.forgetPassword,name="forgetPassword"),
    path('otp/', views.otp,name="otp"),
    path('setNewPassword/', views.setNewPassword,name="setNewPassword"),
]