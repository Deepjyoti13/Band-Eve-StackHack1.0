from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.core import signing
import random
from datetime import datetime
from pytz import timezone
from datetime import timedelta  

# for rendering the landing page 
def index(request):
    return render(request, 'index.html')

#logic associated with url(localhost/form/) 
def form(request):

    # generate a random number to send as otp 
    x = random.randrange(100000, 1000000)
    
    # for post request 
    if request.method == 'POST':
            
            # call Register model class
            data = Register()
            # name 
            data.name = request.POST.get('name')

            # email
            data.email = request.POST.get('email')

            # phonemumber
            data.phoneNumber = request.POST.get('phoneNumber')

            # idcard
            data.idCard = request.FILES.get('idCard')

            # registration type 
            data.regType = request.POST.get('regType')

            # number of tickets
            data.ticketNo = request.POST.get('ticketNo')

            # getting the current time
            utc = datetime.now(timezone('UTC'))
            # storing current time plus one minute
            data.expDate = utc + timedelta(seconds=60)
            
            # random number for otp 
            data.random = x

            # save all data  
            data.save()
            # block to check if email sending was successfull 
            try:
                send_mail(
                'Your OTP is provided below. You are one step away from enrolling yourself!',#email heading
                str(x),#email body
                'bandeve.dad@gmail.com',#email sender
                [data.email],#receivers email
                fail_silently=False,
                )
            except:
                #if email sending failed
                messages.info(request, "Can not send email. Enter a valid email or check your internet connection.")
                return redirect('form')
            # if email sending was successfull
            # dumping the id for improving security           
            value = signing.dumps({"id": data.id})
            return redirect('otp', value)

    # for rendering html 
    return render(request, 'form.html')

# logic for otp verification
def otp(request, pk):
    #loading the primary key 
    signing.loads(pk)
    d = signing.loads(pk)
    # query
    reg = Register.objects.get(id=d['id'])
    if request.method == "POST":
        # if the onetime password given by the user is right 
        if reg.random == int(request.POST.get('onetime')):

            # status is changed to True which by default is false 
            reg.status = True

            # generating registration number 
            reg.random= random.randrange(100000, 1000000)
            reg.save()

            context = {'id': reg.random}
            # sending the confirmation mail with the registration id 
            try:
                send_mail(
                'Your Registration ID is:',
                str(reg.random),
                'bandeve.dad@gmail.com',
                [reg.email],
                fail_silently=False,
                )
            except:
                messages.info(request, "Can not send email. Enter a valid email or check your internet connection.")
                return redirect('otp')
            return render(request, 'thankyou.html', context)
        else:
            # if otp is wrong delete data from database  and redirect to form
            reg.delete()
            messages.info(request, "Invalid OTP. Try again!")
            return redirect('form')
    # for rendering html
    return render(request, 'otp.html')

