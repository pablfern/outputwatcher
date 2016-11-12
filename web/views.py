from web.forms import SearchOutput
from django.shortcuts import render, redirect


def home(request):
    pass


def login(request):
    return render(request, 'web/account/login.html', {})


def register(request):
    return render(request, 'web/account/register.html', {})


def following_outputs(request):
    return render(request, 'web/following_outputs.html', {})


def search_output(request):
    search_form = SearchOutput(request.POST or None)
    if search_form.is_valid():
        return redirect('add_output')

    return render(request, 
                  'web/outputs/search_output.html', 
                  {'search_form': search_form})


def add_output(request):
    return render(request, 'web/outputs/add_output.html', {})
