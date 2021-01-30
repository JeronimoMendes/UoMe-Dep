from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import CustomUserCreationForm
from django.forms import ValidationError
from django.contrib.auth.models import User
from .models import FriendRequest

# Create your views here.
def dashboard2(request):
    return render(request, "users/dashboard2.html")


def welcome(request):
    return render(request, "users/welcome.html")

def dashboard(request):
    context = {}
    if request.user.is_authenticated:
        user = request.user
        profile = user.profile
        network = profile.network.all()
        network = [i.user.username for i in network]
        nr_friend_requests = len(FriendRequest.objects.filter(to_user=user))
        context = {
            "network": network,
            "debt": user.profile.debt / 100,
            "owed": user.profile.owed / 100,
            "nr_friend_requests": nr_friend_requests
        }
        
    return render(request, "users/dashboard.html", context)

def register(request):

    args = {}
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.save()
            login(request, user)
            return redirect("/debt_dashboard/")
        
    else:
        form = CustomUserCreationForm()
    args["form"] = form

    return render(request, "users/register.html", args)

    
def user_search_view(request, *args, **kwargs):

    if not request.user.is_authenticated: return redirect("/accounts/login")
    context = {}
    nr_friend_requests = len(FriendRequest.objects.filter(to_user=request.user))
    context["nr_friend_requests"] = nr_friend_requests

    if(request.GET.get("search-user")):
        redirect("/search?q={}".format(request.GET.get("q").get))

    if(request.GET.get('mybtn')):
        user2 = request.GET.get('user2')
        request.user.profile.request_network(user2)
        return redirect("/search/")

    elif request.method == "GET":
        search_query = request.GET.get("q")

        if search_query == None:
            return render(request, "users/search_results.html", {"search_result":None, "nr_friend_requests": nr_friend_requests})

        if len(search_query) > 0:
            search_result = User.objects.filter(username__icontains=search_query)
            context["search_result"] = [(u, request.user.profile.network.filter(user=u).exists()) for u in search_result]
            context["friend_request_sent"] = [i.to_user for i in FriendRequest.objects.filter(from_user=request.user)]

    return render(request, "users/search_results.html", context)


def friends(request):
    if not request.user.is_authenticated: return redirect("/accounts/login")

    def get_context():
        context = {
            "friends": request.user.profile.network.all(),
            "friend_requests": FriendRequest.objects.filter(to_user=request.user),
            "nr_friend_requests": len(FriendRequest.objects.filter(to_user=request.user))
        }
        return context

    if(request.GET.get('mybtn')):
        user2 = request.GET.get('user2')
        request.user.profile.remove_from_network(user2)
        return redirect("/friends/")

    if(request.GET.get('mybtn_fr')):
        user2 = request.GET.get('friend_request')
        request.user.profile.add_to_network(user2)
        return redirect("/friends/")

    if(request.GET.get("mybtn_fr_reject")):
        user2 = User.objects.get(username=request.GET.get('friend_request'))
        friend_request = FriendRequest.objects.get(from_user=user2, to_user=request.user)
        friend_request.delete()
        return redirect("/friends/")

    if request.method == "GET":
        return render(request, "users/friends.html", get_context()) 
