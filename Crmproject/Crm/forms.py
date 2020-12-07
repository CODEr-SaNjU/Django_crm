from django import forms
from .models import Enquiry
from django.contrib.auth.models import User

from django.http import Http404, HttpResponse
from django.contrib.auth.forms import UserCreationForm


class SalespersonEnquiryForm(forms.ModelForm):
  class Meta:
    model = Enquiry
    fields = ['Contact_number','Email','Name','Company_name','Enquiry_details','City','State']



class salespersonUpdateEnquiryForm(forms.ModelForm):
    class Meta:
        model =Enquiry
        fields = ['enquiry_source','profession','visited_status','Visit_status','expected_purchase_Date','visit_date','Booking_Date','Contact_number','Email','Name','Company_name','Enquiry_details','City','State']
        labels = {
      'Visit_status': ('Enquiry status')
      }

class salespersonstatusEnquiryForm(forms.ModelForm):
  class Meta:
    model = Enquiry
    fields = ['Visit_status','remarks']
    labels = {
      'Visit_status': ('Enquiry status')
      }


class CreateEnquiryForm(forms.ModelForm):
  class Meta:
    model = Enquiry
    fields = ['username','Contact_number','Email','Name','Company_name','Enquiry_details','City','State']
    labels = {
      'username': ('Assign to user')
      }

    
class UpdateEnquiryForm(forms.ModelForm):
  class Meta:
    model = Enquiry
    fields = ['username','enquiry_source','profession','visited_status','Visit_status','Contact_number','Email','Name','Company_name','Enquiry_details','City','State','expected_purchase_Date','visit_date','Booking_Date','remarks']
    labels = {
      'username': ('Assign to user')
      }


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']
        widgets = {
          'username' : forms.TextInput(attrs={'class':'form-control','id':'usernameid'}),
          'first_name' : forms.TextInput(attrs={'class':'form-control','id':'first_nameid'}),
          'email' : forms.EmailInput(attrs={'class':'form-control','id':'emailid'}),
          'password1' : forms.PasswordInput(attrs={'class':'form-control','id':'password1id'}),
          'password2' : forms.PasswordInput(attrs={'class':'form-control','id':'password2id'}),
        }
        labels = {
            'first_name': ('full Name')
        }
