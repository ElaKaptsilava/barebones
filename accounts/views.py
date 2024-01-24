from django.shortcuts import render

from accounts.forms import CustomUserCreationForm


def home(request):
    return render(request, 'accounts/home.html')


def register(request):
    form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {form: 'form'})
