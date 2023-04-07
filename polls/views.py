from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import User
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    current = request.session['user']
    return render(request, 'polls/index.html', {'username': current})


def user(request):
    name = None
    if request.GET.get('name'):
        # A03:2021 – Injection
        # you can get the information of any user by using a parameter
        # fix this by checking that parameter is the same as current user in session
        name = request.GET.get('name')
    try:
        user_obj = User.objects.get(username=name)
    except:
        user_obj = None
    return render(request, 'polls/user.html', {'name': name, 'user': user_obj})


def login(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.get(username=username)
            if (user.password != password):
                # A09:2021 - Security Logging and Monitoring Failures
                # no logging with failed attempt to log in
                # print('failed to log in with username', username)
                return redirect('/loginView')
            request.session['user'] = user.username
            if user.username == 'admin':
                return redirect('/admin')
        except:
            return redirect('/loginView')
    return redirect('/')


def loginView(request):
    return render(request, 'polls/login.html')


def logout(request):
    request.session['user'] = None
    return redirect('/')


def admin(request):
    if not request.session['user']:
        return redirect('/')
    # A01:2021 – Broken Access Control
    # any user can access the admin endpoint that reveals all usernames and passwords
    # limit access to this to only admin
    all_users = User.objects.all()
    return render(request, 'polls/admin.html', {'users': list(all_users)})


def create(request):
    if request.method == 'POST':
        # A02:2021 – Cryptographic Failures
        # passwords are not crypted before they are saved to the database
        # fix by using some kind of encryption
        user = User(username=request.POST.get('username'),
                    password=request.POST.get('password'))
        # A07:2021 – Identification and Authentication Failures
        # weak passwords allowed, same username and password allowed
        # fix by adding some type of password analysis / check
        user.save()
        request.session['user'] = user.username
        return redirect('/')
    return render(request, 'polls/create.html')
