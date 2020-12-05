from django import forms
from .models import Enquiry
from django.contrib.auth.models import User

from django.http import Http404, HttpResponse
from django.contrib.auth.forms import UserCreationForm





class EnquiryForm(forms.ModelForm):
    class Meta:
        model =Enquiry
        fields = ['username','enquiry_source','profession','visited_status','Visit_status','Contact_number','Email','Name','Company_name','Enquiry_details','City','State','expected_purchase_Date','visit_date','Booking_Date','remarks']
        widgets = {
          'Contact_number' : forms.TextInput(attrs={'class':'form-control','id':'rnid'}),
          'QUERY_ID' : forms.TextInput(attrs={'class':'form-control','id':'queryid'}),
          'QTYPE' : forms.TextInput(attrs={'class':'form-control','id':'qtypeid'}),
          'Email' : forms.TextInput(attrs={'class':'form-control','id':'Emailid'}),
          'MOB' : forms.TextInput(attrs={'class':'form-control','id':'MOBid'}),
          'QUERY_MODID' : forms.TextInput(attrs={'class':'form-control','id':'QUERY_MODIDid'}),
          'GLUSR_USR_COMPANYNAMEid' : forms.TextInput(attrs={'class':'form-control','id':'GLUSR_USR_COMPANYNAMEid'}),
          'ENQ_MESSAGE':forms.Textarea(attrs={'class':'form-control'})

        }
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
