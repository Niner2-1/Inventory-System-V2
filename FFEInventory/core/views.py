from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def dashboard(request):
    return render(request, "pages/dashboard.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "pages/login.html", {"error": "Invalid username or password"})
    else:
        return render(request, "pages/login.html")
    
def logout_view(request):
    logout(request)
    return redirect("login")
