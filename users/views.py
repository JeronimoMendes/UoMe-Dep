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
            {"form": AddToNetwork()}
        )

    if request.method == "POST":
        form = AddToNetwork(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()

    return redirect("/edit_info/")

    
def user_search_view(request, *args, **kwargs):
    if not request.user.is_authenticated: return redirect("/accounts/login")
    context = {}

    if(request.GET.get('mybtn')):
        user2 = request.GET.get('user2')
        request.user.profile.request_network(user2)

    elif request.method == "GET":
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            search_result = User.objects.filter(username__icontains=search_query)
            context["search_result"] = [(u, request.user.profile.network.filter(user=u).exists()) for u in search_result]

    return render(request, "users/search_results.html", context)


def friend_request(request):
    if(request.GET.get('mybtn')):
        user2 = request.GET.get('user2')
        request.user.profile.add_to_network(user2)


    if request.method == "GET":
        context = {}
        friend_requests = request.user.profile.network_requests.all()
        friend_requests = [i.user for i in friend_requests]

        context = {"friend_requests": friend_requests}
        print(context)
        return render(request, "users/friend_requests.html", context)