from django.db import models


# Create your models here.
class Register(models.Model):
    # registration type 
    regChoice = (
        ('Self', 'Self'),
        ('Group', 'Group'),
        ('Corporate', 'Corporate'),
        ('Others', 'Others'),
    )
    # stores name 
    name = models.CharField(max_length=50)
    
    # stores email 
    email = models.EmailField(max_length=254, null=True)
    
    # stores phonenumber
    phoneNumber = models.CharField(max_length=50)

    # stores idcard
    idCard = models.ImageField(upload_to='idCard', null=True)

    # stores registration type 
    regType = models.CharField(max_length=25, choices=regChoice,null=True)
    
    # stores number of tickets
    ticketNo = models.CharField(max_length=20, null=True)

    # stores time and date of form creation 
    date = models.DateTimeField(auto_now=True)

    #stores time and date for otp verification
    expDate = models.DateTimeField(null=True)

    # a booleanfield to store the status of the form 
    status = models.BooleanField(default=False)

    # to srore registration id 
    random = models.IntegerField(null=True)

    def __str__(self):
        return self.name