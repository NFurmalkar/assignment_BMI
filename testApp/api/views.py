from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from testApp.api.serializers import userSerializer
from django.contrib.auth.models import User
from django.shortcuts import redirect
import random
from django.contrib.auth.hashers import make_password

class checkEmail(APIView):
    def post(self,request,pk):
        data = request.data
        email = request.data.get('email')
        isValid = User.objects.filter(email=email).exists()
        if isValid:
            return Response({'msg':'Invalid Email'},status=status.HTTP_404_NOT_FOUND)

        # Send email
        otp = str(random.randint(0000, 9999))
        try:
            sub = "Tax Bucket"
            mess = f"Your OTP is :{otp}"
            to = email.strip()
            # send_mail(sub,mess,".....@gmail.com",[to])
            request.session['otp'] = otp
            request.session['email'] = to
        except Exception as e:
            print("error in email", e)
            return Response({'msg': "Please check connection or email"})
        return Response({'msg':'Email exists'},status=status.HTTP_200_OK)

class checkOTP(APIView):
    def post(self,request):
        sysOTP = request.session.get('otp')
        userOTP = request.data.get('otp')

        if sysOTP == None or userOTP == None:
            return Response({'msg':"Invalid"})
        return Response({'msg':"otp matched"},status=status.HTTP_200_OK)

class changePassword(APIView):
    def post(self,request):
        email = request.session['email']
        password = request.data.get('password')
        HashPassword = make_password(password)
        user = User.objects.get(email=email)
        user.password = HashPassword
        user.save()
        return Response({'msg':'password changed successfully'},status=status.HTTP_200_OK)