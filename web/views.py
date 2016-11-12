from django.shortcuts import render

# Create your views here.


def home(request):
    pass


def login(request):
    return render(request, 'web/account/login.html', {})


def register(request):
    return render(request, 'web/account/register.html', {})


def following_outputs(request):
    return render(request, 'web/following_outputs.html', {})


def add_output(request):
    return render(request, 'web/add_output.html', {})
