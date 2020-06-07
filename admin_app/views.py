from django.shortcuts import render, redirect
from event.models import *
from django.contrib import messages
from django.contrib.auth.models import User, auth, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url="manager_login")
# admin view
def admin_page(request):
    data = Register.objects.all()
    Self = Register.objects.filter(regType="Self").count()
    Group = Register.objects.filter(regType="Group").count()
    Corporate = Register.objects.filter(regType="Corporate").count()
    Others = Register.objects.filter(regType="Others").count()
    Total = Self+Group+Corporate+Others
    context = {
        "data": data,
        "Self": Self,
        "Group": Group,
        "Corporate": Corporate,
        "Others": Others,
        "Total": Total,
    }
    return render(request, "admin_page.html", context)




# function to grant access to manager only
def manager_login(request):

    if request.user.is_authenticated:
        return redirect("admin_page")

    # if request is of post type
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        # authenticate username and password
        user = auth.authenticate(username=username, password=password)

        # if username and login is valid

        if user is not None:
            auth.login(request, user)

            # redirect to admin dashboard
            return redirect("admin_page")

        # if invalid credentials is given show message and redirect to the same page
        else:
            messages.info(request, "invalid credentials")
            return redirect("manager_login")

    else:
        return render(request, "login.html", {"act": manager_login})


# logout
def manager_logout(request):
    auth.logout(request)
    return redirect("manager_login")

@login_required(login_url="manager_login")
def profile(request, key):
    data = Register.objects.get(id=key)
    context = {"data": data}
    return render(request, "profile.html", context)

