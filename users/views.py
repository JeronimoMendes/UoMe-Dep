from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import CustomUserCreationForm, AddToNetwork
from django.forms import ValidationError
from django.contrib.auth.models import User

# Create your views here.

def dashboard(request):
    user = request.user
    profile = user.profile
    network = profile.network.all()
    network = [i.user.username for i in network]
    args = {}
    args["network"] = network
    return render(request, "users/dashboard.html", args)

def register(request):
    """
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    """
    args = {}
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.save()
            login(request, user)
            return redirect(reverse("dashboard"))
        
    else:
        form = CustomUserCreationForm()
    args["form"] = form

    return render(request, "users/register.html", args)
    
def edit_info(request):
    if request.method == "GET":
        return render(
            request, "users/edit_info.html",
            {"form": AddToNetwork}
        )

    if request.method == "POST":
        form = AddToNetwork(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()

            return redirect(reverse("dashboard"))

    

