from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.core import signing
import random
from datetime import datetime
from pytz import timezone
from datetime import timedelta  


# Create your views here.
def index(request):
    return render(request, 'index.html')

def form(request):
    x = random.randrange(100000, 1000000)
    
    if request.method == 'POST':
        if Register.objects.filter(email=request.POST.get('email')).exists():
                messages.info(request,'Email taken')
                return redirect('form')
        if Register.objects.filter(phoneNumber=request.POST.get('phoneNumber')).exists():
                messages.info(request,'Phone number taken')
                return redirect('form')
        else:
            data=Register()
            data.name = request.POST.get('name')
            data.email = request.POST.get('email')
            data.phoneNumber = request.POST.get('phoneNumber')
            data.idCard = request.FILES.get('idCard')
            data.regType = request.POST.get('regType')
            data.ticketNo = request.POST.get('ticketNo')
            # exp date  
            utc = datetime.now(timezone('UTC'))
            data.expDate=utc+timedelta(seconds=60)
            data.random = x
            data.save()
            try:
                send_mail(
                'Your OTP is provided below. You are one step away from enrolling yourself!',
                str(x),
                'bandeve.dad@gmail.com',
                [data.email],
                fail_silently=False,
                )
            except:
                messages.info(request, "Can not send email. Enter a valid email or check your internet connection.")
                return redirect('form')                
            value = signing.dumps({"id": data.id})
            return redirect('otp', value)
            # return redirect('preview', pk=instance.id)
    return render(request, 'form.html')

def otp(request, pk):
    signing.loads(pk)
    d=signing.loads(pk)
    reg = Register.objects.get(id=d['id'])
    if request.method == "POST":
        if reg.random == int(request.POST.get('onetime')):
            reg.status = True
            reg.random= random.randrange(100000, 1000000)
            reg.save()
            context = {'id': reg.random}
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
            return render(request, 'thankyou.html', context)
        else:
            reg.delete()
            messages.info(request, "Invalid OTP. Try again!")
            return redirect('form')
    return render(request, 'otp.html')

