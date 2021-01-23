from django.shortcuts import render
from .models import CommonAccount
from users.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from users.models import FriendRequest
# Create your views here.
def debt_dashboard(request):   
    def get_context():
        user = request.user
        nr_friend_requests = len(FriendRequest.objects.filter(to_user=user))

        common_accs = [(i, i.other_user(user.username), i.how_much_debt(user)/100) for i in CommonAccount.objects.filter(user1=user)]
        common_accs += [(i, i.other_user(user.username), i.how_much_debt(user)/100) for i in CommonAccount.objects.filter(user2=user)]
        friends = [i.user.username for i in user.profile.network.all() if i.user not in [i for a,i,b in common_accs]]

        context = {
            "common_accs": common_accs,
            "friends": friends,
            'nr_friend_requests': nr_friend_requests
        }
        return context

    if request.GET.get("friend"):
        friend = request.GET['friend'] 

        CommonAccount.objects.create(user1=request.user, user2=User.objects.get(username=friend))
        return redirect("/debt_dashboard/")

    if request.method == "GET":
        return render(request, "dashboard/dashboard.html", get_context())
 

def common_acc(request):
    def get_context():
        query = request.GET.get("q")
        account = CommonAccount.objects.get(id=query)
        user = request.user
        nr_friend_requests = len(FriendRequest.objects.filter(to_user=user))

        context = {
            "other_user": account.other_user(user.username),
            "debt": account.how_much_debt(user.username)/100,
            "owed": account.how_much_owes(user.username)/100,
            "acc": account,
            'nr_friend_requests': nr_friend_requests
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

        return redirect("/common_account/?q={}".format(account_id))

    
    if request.GET.get("inc_owed"):
        inc_debt = float(request.GET.get('value_inc_owed'))
        account_id = request.GET.get('account')
        print(inc_debt)

        account = CommonAccount.objects.get(id=account_id)

        account.decrease_debt(request.user, int(inc_debt*100))

        return redirect("/common_account/?q={}".format(account_id))
