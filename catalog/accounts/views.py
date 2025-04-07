from django.shortcuts import render, redirect
from accounts.forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
            form = RegisterForm()
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next')
            return redirect(next_url or "index")
        else:
            return render(request, 'login.html', {'error': 'Incorrect login or password'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile_view(request):
    return render(request, 'profile.html')
