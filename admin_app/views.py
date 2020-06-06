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


# sign in option
def sign_in_up(request):
    return render(request, "manager.html")


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


# to create new manager account
def manager_register(request):
    if request.user.is_authenticated:
        return redirect("admin_page")
    # if request is of post type
    if request.method == "POST":

        # take the necessay fiels in its respective variables

        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        # if password and confirm password is equal
        if password1 == password2:
            # checks if username is already taken
            if User.objects.filter(username=username).exists():
                messages.info(request, "username taken")
                return redirect("manager_register")

            # checks if the email is already taken
            elif User.objects.filter(email=email).exists():
                messages.info(request, "email taken")
                return redirect("manager_register")

            # create an account and redirect to login page
            else:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password1,
                )
                user.save()
                group = Group.objects.get(name="manager")
                group.user_set.add(user)
                return redirect("manager_login")

        else:
            messages.info(request, "password not matching")
            return redirect("manager_register")

    else:
        return render(request, "register.html")


# logout
def manager_logout(request):
    auth.logout(request)
    return redirect("manager_login")

@login_required(login_url="manager_login")
def profile(request, key):
    data = Register.objects.get(id=key)
    context = {"data": data}
    return render(request, "profile.html", context)

