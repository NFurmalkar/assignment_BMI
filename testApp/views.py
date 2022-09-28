from django.shortcuts import render,redirect
from . models import Details
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
import random
import json
from django.core.mail import send_mail
from django.http import JsonResponse,Http404

# Create your views here.

def regi(request):
    return render(request,'testApp/login.html')

def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email,password)
        if User.objects.filter(email=email).exists():
            messages.error(request,"Email Already exists")
            return redirect("/register")
        user = User(email=email,username=email,password=make_password(password))
        user.save()
        return redirect('/login')
    return render(request,'testApp/register.html')

def getOTP(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        if User.objects.filter(email=email).exists():
            params = {"errorMessage":"Email Already Registered"}
            return JsonResponse(params)
        otp = str(random.randint(0000,9999))
        print(otp)
        # Send email
        try:
            sub = "Tax Bucket"
            mess = f"Your OTP is :{otp}"
            to = email.strip()
            #send_mail(sub,mess,"gavarthor@gmail.com",[to])
        except Exception as e:
            print("error in email",e)
            return JsonResponse({'errorMessage':"Please check connection or email"})
        return JsonResponse({'otp':otp})

def loginUser(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
        user = auth.authenticate(request,username=email,password=password)
        print("=========",user)
        if user is not None:
            auth.login(request,user)
            return redirect('/home')
        else:
            messages.success(request,'Email or password is Incorrect')
            return redirect('/login')
    return render(request, 'testApp/login.html')

def logoutUser(request):
    logout(request)
    messages.error(request,"Logout")
    return redirect('/login')

def home(request):
    if request.user.is_authenticated:
        user = request.user.id
        data = Details.objects.filter(userId_id=user)

        param = {'data':data}
        return render(request,'testApp/home.html',param)
    return redirect('/login')

def addBMI(request):
    userId = request.user.id
    user = User.objects.get(id=userId)
    name = request.POST.get("name")
    gender = request.POST.get("gender")
    height = request.POST.get("height")
    weight = request.POST.get("weight")
    #bmi = request.POST.get("bmi")
    bmi = float(weight)/float(height)
    print(bmi)
    details = Details(userId=user,name=name,gender=gender,height=height,weight=weight,bmi=bmi)
    details.save()
    return redirect('/home')

def updateBMI(request,id):
    userId = request.user.id
    user = User.objects.get(id=userId)
    name = request.POST.get("name")
    gender = request.POST.get("gender")
    height = request.POST.get("height")
    weight = request.POST.get("weight")
    #bmi = request.POST.get("bmi")
    bmi = float(weight)/float(height)
    print(bmi)
    #
    details = Details.objects.get(id=id)
    details.name = name
    details.gender = gender
    details.height = height
    details.weight = weight
    details.bmi = bmi
    details.save()
    return redirect('/home')

def deleteBMI(request,id):
    details = Details.objects.get(id=id)
    details.delete()
    return redirect('/home')

#

# Forget Password
def forgetPassword(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            request.session['BMIEmail'] = email
            otp = str(random.randint(0000,9999))
            #request.session['userEmail'] = emailTP send on email
            try:
                sub = "BMI Application"
                mess = f"Your OTP is {otp}."
                to = email
                #send_mail(sub,mess,"....@gmail.com",[to])
            except Exception as e:
                print("error-------->",e)
                return redirect("/forget-password")
            request.session['BMIOtp'] = otp
            print("otp==========", otp)

            return render(request,'testApp/otp.html')
        else:
            messages.error(request,"This email is not exists")
            return redirect('/forgetPassword')
    return render(request,'testApp/forget-password.html')


def otp(request):
    if request.method == "POST":
        userOtp = request.POST.get("otp")
        otp = request.session.get("BMIOtp")
        print("====>",otp)
        if otp == None:
            return redirect("/forget-password")
        if userOtp == otp:
            return render(request,'testApp/set-new-password.html')
        else:
            messages.error(request,"Invalid OTP")
            return render(request, 'testApp/otp.html')

def setNewPassword(request):
    if request.method == "POST":
        passwordBMI = request.POST.get("password")
        EmailBMI = request.session.get("BMIEmail")
        if EmailBMI == None:
            return redirect("/forget-password")
        password =make_password(passwordBMI)
        print(password)
        user = User.objects.get(email=EmailBMI)
        user.password = password
        user.save()
        messages.success(request,"Password changed successfully.. Please Login")
        return redirect("/login")