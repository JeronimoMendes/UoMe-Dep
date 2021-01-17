from django.shortcuts import render
from .models import CommonBalance
from users.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

# Create your views here.
def debt_dashboard(request):
    if request.method == "GET":
        user = request.user
        common_accs = [(i, i.other_user(user), i.how_much_debt(user)) for i in CommonBalance.objects.filter(user1=user)]
        common_accs += [(i, i.other_user(user), i.how_much_debt(user)) for i in CommonBalance.objects.filter(user2=user)]
        context = {"common_accs":common_accs,}
        return render(request, "dashboard/dashboard.html", context)
