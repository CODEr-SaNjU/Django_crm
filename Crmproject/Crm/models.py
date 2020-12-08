from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.



STATUS = (
    (0,"Yes"),
    (1,"No")
)



class visit_status_time(models.Model):
    last_updtae = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.last_updtae





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


class Enquiry(models.Model):
    username = models.ForeignKey(User, verbose_name='username', on_delete=models.CASCADE ,blank=True,null=True )
    Enquiry_number = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4().hex[:8])
    Contact_number = models.CharField(max_length=12,unique=True)
    Email = models.CharField(max_length=100,) 
    Name = models.CharField(max_length=100,) 
    Company_name = models.CharField(max_length=500,)
    Enquiry_details = models.CharField(max_length=500,)
    City = models.CharField(max_length=100,)
    State = models.CharField(max_length=100,) 
    enquiry_source = models.ForeignKey(Enquiry_Source,on_delete=models.CASCADE,null=True,blank=True )
    expected_purchase_Date = models.DateField(verbose_name='Expected Purchase Date',auto_now_add=False,blank=True,null=True)
    profession = models.ForeignKey(Profession,on_delete=models.CASCADE,null=True,blank=True )
    visit_date = models.DateField(verbose_name='Visit Date',auto_now_add=False,blank=True,null=True)
    visited_status = models.IntegerField(choices=STATUS, default=1)
    Visit_status = models.ForeignKey(Client_Visit,on_delete=models.CASCADE,null=True,blank=True )
    Booking_Date = models.DateField(verbose_name='Booking Date',auto_now_add=False,blank=True,null=True)
    remarks  = models.TextField(blank=True,null=True)
    last_update = models.ForeignKey(visit_status_time,on_delete=models.CASCADE,null=False,blank=False)

    def __str__(self):
        return self.Enquiry_number

