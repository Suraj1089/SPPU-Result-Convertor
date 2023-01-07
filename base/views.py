from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'inc/index.html')

def services(request):
    return render(request,'inc/index.html')

def login(request):
    return render(request,'authentication/login.html')


def register(request):
    return render(request,'authentication/register.html')