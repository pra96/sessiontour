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
                    del request.session['id']
                    del request.session['username']
                    del request.session['is_authenticated']
                except:
                    print("no session record present")
                request.session['id'] = user.id
                request.session['username'] = user.username
                request.session['first_name'] = user.first_name
                request.session['is_authenticated'] = True
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
            if User.objects.filter(username=username).exists():
                messages.info(request, f'Username {username} is Already exits')
                return render(request, 'user/login.html')

            if User.objects.filter(email=email).exists():
                messages.info(request, f'{email} is Already registered user, Please Login')
                return render(request, 'user/login.html')
            user = User.objects.create(username= username, email=email, first_name=first_name, last_name=last_name,password=password,is_client = True)
            user.save()
            priceType = request.POST.get('priceType', False)
            fix = request.POST.get('fix', False)
            variable = request.POST.get('variable', False)
            description = request.POST.get('introduction', False)
            destination = request.POST.get('location', False)
            tourType= request.POST.get('tourType', False)
            if fix == "":
                fix = 0 
            if variable == "":
                variable = 0
            GuideInfo.objects.create(
                guide=user,
                priceType=priceType,
                fix_price=fix,
                variable_price=variable,
                description=description,
                destination=destination,
                tourType=tourType
            )    
            messages.success(request, f'{username} is created successfully')
            return render(request, 'user/guide_price.html', {'data':user.id})
    return render(request, 'user/signup.html')


def guideInfoUpdate(request):
    # if request.method == 'POST':
    print(request)
    print(request.POST.__dict__)
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
    messages.success(request, f'{user.username} Profile is updated successfully')
    return redirect('/')
    # return render(request, 'user/login.html')

def logout(request):
    try:
        del request.session['first_name']
        del request.session['username']
        del request.session['id']
        del request.session['is_authenticated']
        messages.success(request, "Logout Successfull")
    except:
        return redirect('/')
    return render(request, 'user/login.html')
