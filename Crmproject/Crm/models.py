from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
import string
import random
from django.core.validators import MaxValueValidator,MinValueValidator,MaxLengthValidator,RegexValidator

from datetime import timezone


STATUS = (
    (0,"Yes"),
    (1,"No")
)





class Enquiry_Source(models.Model):
    enq_source = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.enq_source



class Profession(models.Model):
    profession = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.profession

class Client_Visit(models.Model):
    Visit_status = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.Visit_status


letters = string.ascii_uppercase
Enquiry_number=(''.join(random.choice(letters) for i in range(10)) )




class Enquiry(models.Model):
    username = models.ForeignKey(User, verbose_name='username', on_delete=models.CASCADE ,blank=True,null=True )
    Enquiry_number = models.CharField(max_length=100, blank=True, unique=True, default=Enquiry_number)
    Contact_number = models.CharField(max_length=13,unique=True,validators=[RegexValidator(r'^\d{1,10}$')])
    Email = models.CharField(max_length=100,) 
    Name = models.CharField(max_length=100,) 
    Company_name = models.CharField(max_length=500,)
    Enquiry_details = models.CharField(max_length=500,)
    City = models.CharField(max_length=100,)
    State = models.CharField(max_length=100,) 
    enquiry_source = models.ForeignKey(Enquiry_Source,on_delete=models.CASCADE,null=True,blank=True )
    expected_purchase_Date = models.DateField(verbose_name='Expected Purchase Date',auto_now_add=False,blank=True,null=True)
    profession = models.ForeignKey(Profession,on_delete=models.CASCADE,null=True,blank=True )
    visited_status = models.IntegerField(choices=STATUS, default=1)
    Visit_status = models.ForeignKey(Client_Visit,on_delete=models.CASCADE,null=True,blank=True,default=2)
    Booking_Date = models.DateField(verbose_name='Booking Date',blank=True,null=True)
    Follow_up = models.DateField(verbose_name='Follow Up Date',blank=True,null=True)
    remarks  = models.TextField(blank=True,null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Enquiry_number




class History(models.Model):
    update_by = models.CharField(max_length=100,verbose_name = "Update By" ,blank = True ,null=True)
    Enquiry_number = models.ForeignKey(Enquiry,verbose_name = "Enquiry Number ",on_delete=models.CASCADE,null=True,blank=True)
    Visit_status = models.CharField(max_length=100,verbose_name = "enquiry status")
    enquiry_status_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.update_by

    # def save(self):
    #    super(History, self).save()
    #    History.objects.update(enquiry_status_time=self.visit_date)
