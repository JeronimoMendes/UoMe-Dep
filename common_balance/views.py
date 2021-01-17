from django.shortcuts import render
from .models import CommonAccount
from users.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

# Create your views here.
def debt_dashboard(request):
    def get_context():
        query = request.GET.get("q")
        account = CommonAccount.objects.get(id=query)
        user = request.user

        context = {
            "other_user": account.other_user(user.username),
            "debt": account.how_much_debt(user.username)/100,
            "owed": account.how_much_owes(user.username)/100,
            "acc": account
        }

        return context

    if request.GET.get("q"):
        return render(request, "dashboard/common_account.html", get_context())

    if request.GET.get("inc_debt"):
        inc_debt = float(request.GET.get('value_inc_debt'))
        account_id = request.GET.get('account')
        print(inc_debt)

        account = CommonAccount.objects.get(id=account_id)

        account.increase_debt(request.user, int(inc_debt*100))

        return redirect("/debt_dashboard/?q={}".format(account_id))

    
    if request.GET.get("inc_owed"):
        inc_debt = float(request.GET.get('value_inc_owed'))
        account_id = request.GET.get('account')
        print(inc_debt)

        account = CommonAccount.objects.get(id=account_id)

        account.decrease_debt(request.user, int(inc_debt*100))

        return redirect("/debt_dashboard/?q={}".format(account_id))


    if request.method == "GET":
        user = request.user
        common_accs = [(i, i.other_user(user), i.how_much_debt(user)/100) for i in CommonAccount.objects.filter(user1=user)]
        common_accs += [(i, i.other_user(user), i.how_much_debt(user)/100) for i in CommonAccount.objects.filter(user2=user)]
        context = {"common_accs":common_accs,}
        return render(request, "dashboard/dashboard.html", context)
 
