from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='/login')
def index_request(request):
    user = request.user
    print(user.first_name)
    print(user.last_name)
    context = {'user': user}
    return render(request, 'index.html', context)


def signup_request(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = UserRegistrationForm()
    # print(form)
    context = {'form': form}
    return render(request, 'signup.html', context)


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello!, {user.first_name} {user.last_name}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    context = {"form": form}
    return render(request, 'login.html', context)


def logout_request(request):
    logout(request)
    #messages.success(request, f"Successfully! Logged out.")
    return redirect('/')
