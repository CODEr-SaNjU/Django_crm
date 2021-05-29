from django import forms
from .models import Enquiry
from django.contrib.auth.models import User
from .models import Client_Visit
from django.http import Http404, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator


class DateInput(forms.DateInput):
    input_type = 'date'


class SalespersonEnquiryForm(forms.ModelForm):
    Contact_number = forms.CharField(
        required=True,
        validators=[RegexValidator(
            r"^[0-9-]+$", "Enter a valid phone number.")],
    )

    class Meta:
        model = Enquiry
        fields = ['username', 'Contact_number', 'Email', 'Name',
                  'Company_name', 'Enquiry_details', 'City', 'State']
        labels = {
            'username': ('Assign To Salesperson')
        }


class salespersonUpdateEnquiryForm(forms.ModelForm):
    Contact_number = forms.CharField(
        required=True,
        validators=[RegexValidator(
            r"^[0-9-]+$", "Enter a valid phone number.")],
    )

    class Meta:
        model = Enquiry
        fields = ['Enquiry_source', 'Profession', 'Machine_Name', 'Visited_status', 'Enquiry_status', 'Follow_up', 'Expected_purchase_Date', 'Delivery_date',
                  'Booking_Date', 'Contact_number', 'Email', 'Name', 'Company_name', 'Enquiry_details', 'City', 'State']
        widget = {
            'Expected_purchase_Date': DateInput(attrs={'type': 'date', }),
            'Booking_Date': DateInput(attrs={'type': 'date'}),
            'Follow_up': DateInput()
        }
        labels = {
            'Enquiry_status': ('Enquiry status'),
            'Visited_status': ('visit status')
        }


class salespersonstatusEnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['Enquiry_status', 'Remarks']
        labels = {
            'Enquiry_status': ('Enquiry status')
        }


class CreateEnquiryForm(forms.ModelForm):
    Contact_number = forms.CharField(
        required=True,
        validators=[RegexValidator(
            r"^[0-9-]+$", "Enter a valid phone number.")],
    )

    class Meta:
        model = Enquiry
        fields = ['username', 'Contact_number', 'Email', 'Name',
                  'Company_name', 'Enquiry_details', 'City', 'State']
        labels = {
            'username': ('Assign To A Salesperson')
        }


class UpdateEnquiryForm(forms.ModelForm):
    Contact_number = forms.CharField(
        required=True,
        validators=[RegexValidator(
            r"^[0-9-]+$", "Enter a valid phone number.")],
    )

    class Meta:
        model = Enquiry
        fields = ['username', 'Enquiry_source', 'Profession', 'Machine_Name', 'Visited_status', 'Enquiry_status', 'Follow_up', 'Expected_purchase_Date', 'Delivery_date',
                  'Booking_Date', 'Remarks', 'Contact_number', 'Email', 'Name', 'Company_name', 'Enquiry_details', 'City', 'State']
        labels = {
            'username': ('Assign To Salesperson'),
            'Visited_status': ('visist status')
        }
        widget = {
            'Expected_purchase_Date': DateInput(attrs={'type': 'date'}),
            'Booking_Date': DateInput(attrs={'type': 'date'}),
        }


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'Usernameid'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'first_nameid'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'emailid'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1id'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2id'}),
        }
        labels = {
            'first_name': ('full Name')
        }
