from django.contrib import admin
from django.urls import path,include
from testApp.api import views
urlpatterns = [
    path('checkEmail/',views.checkEmail.as_view()),
    path('checkOTP/',views.checkOTP.as_view()),
    path('changePassword/',views.changePassword.as_view()),
]