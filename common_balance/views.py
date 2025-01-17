from django.shortcuts import render
from .models import CommonAccount, Log
from users.models import Profile, FriendRequest
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import os
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

    if not request.user.is_authenticated: return redirect("/accounts/login")
    

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
        logs = Log.objects.filter(common_account=account).order_by('-date')

        context = {
            "other_user": account.other_user(user.username),
            "debt": account.how_much_debt(user.username)/100,
            "owed": account.how_much_owes(user.username)/100,
            "acc": account,
            'nr_friend_requests': nr_friend_requests,
            "logs": logs
        }

        return context

    if not request.user.is_authenticated: return redirect("/accounts/login")


    if request.GET.get("q"):
        return render(request, "dashboard/common_account.html", get_context())

    if request.GET.get("submit"):
        print(request.GET.get('value_inc_debt'))
        print(request.GET.get('value_inc_owed'))
        inc_debt = float(request.GET.get('value_inc_debt'))
        inc_owed = float(request.GET.get('value_inc_owed'))
        reason = request.GET.get('reason')

        account_id = request.GET.get('account')
        account = CommonAccount.objects.get(id=account_id)

        account.increase_debt(request.user, int(inc_debt*100))
        account.decrease_debt(request.user, int(inc_owed*100))

        Log.objects.create(by_user=request.user, common_account=account, reason=reason, inc_debt=inc_debt, inc_owed=inc_owed)
        user2 = account.other_user(request.user.username)    

        if user2.profile.email_notification:

            template_context = {
                "account": account,
                "user": request.user,
                "user2": user2,
                "change": inc_debt - inc_owed,
                "minus_change": -(inc_debt - inc_owed),
                "in_debt": account.how_much_debt(user2) > account.how_much_owes(user2),
                "balance": abs(account.balance/100),
                "reason": reason
            }
            template = render_to_string("emails/notification_email.html", template_context)
            
            email = EmailMessage(
                "{} updated your common account".format(request.user),
                template,
                os.getenv("EMAIL_HOST_USER"),
                [user2.email],
            )

            try:
                email.fail_silently = True
                email.send()
            except:
                print("Notification failed!")
        
        return redirect("/common_account/?q={}".format(account_id))
