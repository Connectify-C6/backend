from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/auth/login')
def index(request):
    return JsonResponse({"Message":"Hello World"})

@csrf_exempt
def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid(): 
            user = form.save()
            user_profile = UserProfile(
                user=user, 
                role="common_user",
                bio="",
                count_reported=0
            )
            user_profile.save()
            return redirect('login:login_user')
    else:
        form = UserCreationForm()
    context = {"form": form}
    return render(request, "register.html", context)

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(
            request, 
            username=username, 
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect("login:index")
    else:
        return render(request, "login.html")

@csrf_exempt
def logout_user(request):
    logout(request) 
    return redirect("login:login_user")