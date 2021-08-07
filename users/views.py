import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.contrib.auth import login
from huecotours.models import GuideInfo
from django.urls import re_path
# Create your views here.

def login(request):
    if request.method == 'POST':
        email = request.POST.get("email", False)
        password = request.POST.get("password", False)
        if email and password:
            try:
                user = User.objects.get(email=email, password=password)
                try:
                    del request.session['first_name']
                    del request.session['username']
                    del request.session['is_authenticated']
                    del request.session['is_guide']
                except:
                    print("not logged in")
                request.session['username'] = user.username
                request.session['first_name'] = user.first_name
                request.session['is_authenticated'] = True
                request.session['is_guide'] = user.is_guide
                messages.success(request, "Login Successfull")
                return redirect('/')
            except User.DoesNotExist as e:
                messages.info(request, "Invalid Credentials")
                return redirect("login")
    return render(request, 'user/login.html')

def signup(request):
    if request:
        if request.method == 'POST':
            first_name = request.POST.get('first_name', False)
            last_name = request.POST.get('last_name', False)
            username = request.POST.get('username', False)
            password = request.POST.get('password', False)
            email = request.POST.get('email', False)
            is_guide = request.POST.get('is_guide', False)
            if User.objects.filter(username=username).exists():
                messages.info(request, f'Username {username} is Already exits')
                return render(request, 'user/login.html')

            if User.objects.filter(email=email).exists():
                messages.info(request, f'{email} is Already registered user, Please Login')
                return render(request, 'user/login.html')
            if is_guide == False:
                is_guide = False
                is_client = True
            else:
                is_client = False
                is_guide = True
            user = User.objects.create(username= username, email=email, first_name=first_name, last_name=last_name, is_guide=is_guide, is_client=is_client,password=password)
            user.save()
            if is_guide:
                GuideInfo.objects.create(
                    guide=user,
                    priceType='fix',
                    fix_price=0,
                    variable_price=0
                )
                messages.success(request, 'Please login and complete profile info from Update Info Button')
            messages.success(request, f'{username} is created successfully')
            return redirect('login')
    return render(request, 'user/signup.html')


def guideInfoUpdate(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.session['username'], first_name = request.session['first_name'])
        priceType = request.POST.get('priceType', False)
        fix = request.POST.get('fix', False)
        variable = request.POST.get('variable', False)
        description = request.POST.get('introduction', False)
        destination = request.POST.get('location', False)
        if fix == "":
            fix = 0 
        if variable == "":
            variable = 0
        guide = GuideInfo.objects.get(guide= user)
        guide.priceType = priceType
        guide.fix_price = fix
        guide.variable_price = variable
        guide.description = description
        guide.destination = destination
        guide.save()
        messages.success(request, f'{user.username} Fees is updated successfully')
        return redirect('/')
    return render(request, 'user/guide_price.html')

def logout(request):
    try:
        del request.session['first_name']
        del request.session['username']
        del request.session['is_authenticated']
        del request.session['is_guide']
        messages.success(request, "Logout Successfull")
    except:
        return redirect('/')
    return render(request, 'user/login.html')
