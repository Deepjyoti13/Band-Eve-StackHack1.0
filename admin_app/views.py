from django.shortcuts import render, redirect
from event.models import *
from django.contrib import messages
from django.contrib.auth.models import User, auth, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# to ensure the user is logged in 
@login_required(login_url="manager_login")
# admin landing page
def admin_page(request):
    # guery
    data = Register.objects.all()

    # count number of registrations per group type
    Self = Register.objects.filter(regType="Self").filter(status="True").count()
    Group = Register.objects.filter(regType="Group").filter(status="True").count()
    Corporate = Register.objects.filter(regType="Corporate").filter(status="True").count()
    Others = Register.objects.filter(regType="Others").filter(status="True").count()
    
    # total no of registration
    Total = Self + Group + Corporate + Others
    
    context = {
        "data": data,
        "Self": Self,
        "Group": Group,
        "Corporate": Corporate,
        "Others": Others,
        "Total": Total,
    }
    return render(request, "admin_page.html", context)




# function to grant admin to admin only
def manager_login(request):
    # if already logged in redirect to admin landing page 
    if request.user.is_authenticated:
        return redirect("admin_page")

    # if request is of post type
    if request.method == "POST":
        
        # get username and password 
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
        # render html 
        return render(request, "login.html", {"act": manager_login})


# logout session
def manager_logout(request):
    auth.logout(request)

    # redirect to login page 
    return redirect("manager_login")

# ensuring only admin can access the page 
@login_required(login_url="manager_login")

# to see the registration information
def profile(request, key):
    data = Register.objects.get(id=key)
    context = {"data": data}
    return render(request, "profile.html", context)

