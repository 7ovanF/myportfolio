from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.http import FileResponse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import datetime

from main.views import base_context;

def favicon(request):
    file = (settings.BASE_DIR / "favicon.ico").open("rb")
    return FileResponse(file)

# =====
# USERS
# =====

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("login_user")

    context = {
        **base_context,
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        login(request, user=form.get_user())
        response = redirect("main:landing_page")
        response.set_cookie("last_login", value=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response
    
    context = {
        **base_context,
        "form": form
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:landing_page")
    response.delete_cookie('last_login')
    return response