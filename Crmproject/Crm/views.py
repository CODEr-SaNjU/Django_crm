from django.shortcuts import render,redirect , get_object_or_404
from django.contrib.auth.models import User,auth ,Group
from django.http import Http404, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect , get_object_or_404
from django.contrib.auth.models import User,auth ,Group
from django.http import Http404, HttpResponse
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib import messages
import csv,io
from django.contrib.auth import authenticate,get_user_model
from django.contrib import auth 
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from . decorators import unauthenticated_user ,allowed_user ,admin_only  
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
import os
from django.http import JsonResponse
from . forms import UserForm ,SalespersonEnquiryForm ,CreateEnquiryForm ,UpdateEnquiryForm , salespersonUpdateEnquiryForm,salespersonstatusEnquiryForm
import requests
from django.db.models import Q
import json
from django.conf import  settings
from django.urls import reverse_lazy
from .models import Enquiry,Enquiry_Source,Profession,Client_Visit
from django.template.loader import render_to_string
import datetime 
import pytz 



@unauthenticated_user
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']   
        user = auth.authenticate(username=email,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('Admin_panel')
        else:
            messages.error(request, 'Error! please enter the correct  Username and Password for a staff account.')
            return render(request,'html_files/login.htm')

    else:
        return render(request,"html_files/login.htm")

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect("login")


@login_required(login_url='login')
@admin_only
def Admin_panel(request):
    if request.method == "POST":
        userform = UserForm(request.POST)
        if userform.is_valid():
            user = userform.save()
            messages.success(request, f'Registration complete! You may log in!')
    else:
        userform = UserForm(request.POST)
    all_user = User.objects.all()

    all_enq = Enquiry.objects.all()
    paginator = Paginator(all_enq,10)
    page_number = request.GET.get('page')
    page_obj_all_enq= paginator.get_page(page_number)
    total_enquiry_data = all_enq.count()

    assign_enq = Enquiry.objects.filter(username__isnull=False)
    paginator = Paginator(assign_enq,10)
    page_number = request.GET.get('page')
    page_obj_assign_enq= paginator.get_page(page_number)
    assign_enq_count = assign_enq.count()

    notassign_enq = Enquiry.objects.filter(username__isnull=True)
    paginator = Paginator(notassign_enq,10)
    page_number = request.GET.get('page')
    page_obj_notassign_enq= paginator.get_page(page_number)
    notassign_enq_count = notassign_enq.count()
    last_all_enq = Enquiry.objects.filter().order_by('-id')[:14]
    all_enq_in_ascending_order = reversed(last_all_enq)

    return render(request,'html_files/Main.htm',{'last_all_enq':last_all_enq,'total_enquiry_data':total_enquiry_data,'page_obj_all_enq':page_obj_all_enq,'userform': userform, 'all_user':all_user,'page_obj_assign_enq':page_obj_assign_enq,'page_obj_notassign_enq':page_obj_notassign_enq,'assign_enq_count':assign_enq_count,'notassign_enq_count':notassign_enq_count})





def search_enq_month(request):
    try:
        qur = request.GET.get('search')
        qur1 = request.GET.get("search1")
        print(qur)
        print(qur1)
        last_all_enq = Enquiry.objects.filter(Booking_Date__range=(qur,qur1))
        # print(last_all_enq)
        return render(request,'html_files/Main.htm',{"last_all_enq":last_all_enq})
    except:
        return HttpResponse("smothing is wrong")


@admin_only
def Enquiry_search(request):
    try:
        qur = request.GET.get('search')
        last_all_enq = Enquiry.objects.filter(Q(Name__icontains=qur) | Q(Enquiry_number__icontains=qur) | Q(State__icontains=qur) )
        return render(request,'html_files/Main.htm',{"last_all_enq":last_all_enq})
    except:
        return HttpResponse("Cannot use None as a query value")
  



def save_enq_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            IST = pytz.timezone('Asia/Kolkata')
            datetime_ist = datetime.now(IST)
            x = datetime_ist.strftime('%Y:%m:%d %H:%M:%S %Z %z')
            # user.enquiry_status_time = request.user.Booking_Date
            print("sanju",x)
            data['form_is_valid'] = True
            last_all_enq = Enquiry.objects.all()
            last_all_enq = Enquiry.objects.filter().order_by('-id')[:10]
            data['html_enq_list'] = render_to_string('html_files/enq_list.htm',{'last_all_enq':last_all_enq})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
    print("sanju herer",data)


def enq_create(request):
    data = dict()
    if request.method == 'POST':
        form = CreateEnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            last_all_enq = Enquiry.objects.all()
            data['html_enq_list'] = render_to_string('html_files/enq_list.htm',{'last_all_enq':last_all_enq})
        else:
            data['form_is_valid'] =False
    else:
        form = CreateEnquiryForm()
    context={'form':form}
    data['html_form']  = render_to_string('html_files/add_enq.htm',context,request=request)
    return JsonResponse(data)



def Enquiry_Update(request,pk_id):
    obj_update = get_object_or_404(Enquiry,id=pk_id)
    if request.method=="POST":
        form = UpdateEnquiryForm(request.POST, instance=obj_update)
    else:
        form = UpdateEnquiryForm(instance=obj_update)
    return save_enq_form(request,form,'html_files/enquiry_update.htm')
    

def Enquiry_Delete(request,pk_id):
    obj_delete = get_object_or_404(Enquiry,id=pk_id)
    data = dict()
    if request.method == "POST":
        obj_delete.delete()
        data['form_is_valid'] = True
        last_all_enq = Enquiry.objects.filter().order_by('-id')[:10]
        data['html_enq_list'] = render_to_string('html_files/enq_list.htm',{'last_all_enq':last_all_enq})
    else:
        data['html_form'] = render_to_string('html_files/enquiry_delete.htm', {'obj_delete':obj_delete}, request=request)
    return JsonResponse(data)


def save_user_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            all_user = User.objects.all()
            data['html_user_list'] = render_to_string('html_files/all_user_list.htm',{'all_user':all_user})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data) 



def user_update(request,pk_id):
    user_update = get_object_or_404(User,id=pk_id)
    if request.method=="POST":
        form = UserForm(request.POST, instance=user_update)
    else:
        form = UserForm(instance=user_update)
    return save_user_form(request,form,'html_files/user_update.htm')


def user_delete(request,pk_id):
    user_delete = get_object_or_404(User,id=pk_id)
    data = dict()
    if request.method=="POST":
        user_delete.delete()
        data['form_is_valid'] = True
        all_user = User.objects.all()
        data['html_user_list'] = render_to_string('html_files/all_user_list.htm',{'all_user':all_user})
    else:
        data['html_form'] = render_to_string('html_files/user_delete.htm', {'user_delete':user_delete}, request=request)
    return JsonResponse(data)






@login_required(login_url='login')
def saleperson_page(request):
    Hot_enq = Enquiry.objects.filter(Visit_status=1,username=request.user)
    paginator = Paginator(Hot_enq,14)
    page_number = request.GET.get('page')
    page_obj= paginator.get_page(page_number)
    Hot_enq_count = Hot_enq.count()

    cold_enq = Enquiry.objects.filter(username=request.user,Visit_status=2)
    paginator = Paginator(cold_enq,14)
    page_number = request.GET.get('page')
    page_obj_cold_enq= paginator.get_page(page_number)
    cold_enq_count = cold_enq.count()

    pending_enq = Enquiry.objects.filter(username=request.user,Visit_status=3)
    paginator = Paginator(pending_enq,14)
    page_number = request.GET.get('page')
    page_obj_pending_enq= paginator.get_page(page_number)
    pending_enq_count = pending_enq.count()

    delivered_enq = Enquiry.objects.filter(username=request.user,Visit_status=4)
    paginator = Paginator(delivered_enq,14)
    page_number = request.GET.get('page')
    page_obj_delivered_enq= paginator.get_page(page_number)
    delivered_enq_count = delivered_enq.count()

    today_follow_up_enq = Enquiry.objects.filter(username=request.user,Visit_status=5,Follow_up=datetime.datetime.today())
    print(today_follow_up_enq)
    paginator = Paginator(today_follow_up_enq,14)
    page_number = request.GET.get('page')
    page_obj_today_follow_up_enq= paginator.get_page(page_number)
    today_follow_up_enq_count = today_follow_up_enq.count()
    follow_up_enq = Enquiry.objects.filter(username=request.user,Visit_status=5,Follow_up=datetime.datetime.today()+datetime.timedelta(days=2))
    paginator = Paginator(follow_up_enq,14)
    page_number = request.GET.get('page')
    page_obj_follow_up_enq= paginator.get_page(page_number)
    follow_up_enq_count = follow_up_enq.count()



    lost_enq = Enquiry.objects.filter(username=request.user,Visit_status=6)
    paginator = Paginator(lost_enq,14)
    page_number = request.GET.get('page')
    page_obj_lost_enq= paginator.get_page(page_number)
    lost_enq_count = lost_enq.count()
    return render(request,'Salesperson_Dashboard/salesperson.htm',{'page_obj':page_obj,'Hot_enq_count':Hot_enq_count,'page_obj_cold_enq':page_obj_cold_enq,'cold_enq_count':cold_enq_count,'page_obj_pending_enq':page_obj_pending_enq,'pending_enq_count':pending_enq_count,'delivered_enq_count':delivered_enq_count,'page_obj_delivered_enq':page_obj_delivered_enq,'lost_enq_count':lost_enq_count,'page_obj_lost_enq':page_obj_lost_enq,'page_obj_follow_up_enq':page_obj_follow_up_enq,'follow_up_enq_count':follow_up_enq_count,'today_follow_up_enq':today_follow_up_enq})








def salesperson_save_enq_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            page_obj_cold_enq = Enquiry.objects.filter(username=request.user,Visit_status=2)
            page_obj = Enquiry.objects.filter(Visit_status=1,username=request.user)
            page_obj_pending_enq = Enquiry.objects.filter(username=request.user,Visit_status=3)
            page_obj_delivered_enq = Enquiry.objects.filter(username=request.user,Visit_status=4)
            page_obj_lost_enq = Enquiry.objects.filter(username=request.user,Visit_status=6)
            data['html_enq_list'] = render_to_string('Salesperson_Dashboard/cold_list.htm',{'page_obj_cold_enq':page_obj_cold_enq,'page_obj':page_obj,'page_obj_pending_enq':page_obj_pending_enq,'page_obj_delivered_enq':page_obj_delivered_enq,'page_obj_lost_enq':page_obj_lost_enq})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)



def salesperson_enq_create(request):
    data = dict()
    if request.method == 'POST':
        form = SalespersonEnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            page_obj_cold_enq = Enquiry.objects.filter(username=request.user,Visit_status=2)
            page_obj = Enquiry.objects.filter(Visit_status=1,username=request.user)
            page_obj_pending_enq = Enquiry.objects.filter(username=request.user,Visit_status=3)
            page_obj_delivered_enq = Enquiry.objects.filter(username=request.user,Visit_status=4)
            page_obj_lost_enq = Enquiry.objects.filter(username=request.user,Visit_status=5)
            data['html_enq_list'] = render_to_string('Salesperson_Dashboard/cold_list.htm',{'page_obj_cold_enq':page_obj_cold_enq,'page_obj':page_obj,'page_obj_pending_enq':page_obj_pending_enq,'page_obj_delivered_enq':page_obj_delivered_enq,'page_obj_lost_enq':page_obj_lost_enq})
        else:
            data['form_is_valid'] =False
    else:
        form = SalespersonEnquiryForm()
    context={'form':form}
    data['html_form']  = render_to_string('Salesperson_Dashboard/add_enq.htm',context,request=request)
    return JsonResponse(data)



def salesperson_Enquiry_Update(request,pk_id):
    obj_update = get_object_or_404(Enquiry,id=pk_id)
    if request.method=="POST":
        form = salespersonUpdateEnquiryForm(request.POST, instance=obj_update)
    else:
        form = salespersonUpdateEnquiryForm(instance=obj_update)
    return salesperson_save_enq_form(request,form,'Salesperson_Dashboard/salesenq_update.htm')
    

def salesperson_Enquiry_Delete(request,pk_id):
    obj_delete = get_object_or_404(Enquiry,id=pk_id)
    data = dict()
    if request.method == "POST":
        obj_delete.delete()
        data['form_is_valid'] = True
        page_obj_cold_enq = Enquiry.objects.filter(username=request.user,Visit_status=2)
        page_obj = Enquiry.objects.filter(Visit_status=1,username=request.user)
        page_obj_pending_enq = Enquiry.objects.filter(username=request.user,Visit_status=3)
        page_obj_delivered_enq = Enquiry.objects.filter(username=request.user,Visit_status=4)
        page_obj_lost_enq = Enquiry.objects.filter(username=request.user,Visit_status=5)
        data['html_enq_list'] = render_to_string('Salesperson_Dashboard/cold_list.htm',{'page_obj_cold_enq':page_obj_cold_enq,'page_obj':page_obj,'page_obj_pending_enq':page_obj_pending_enq,'page_obj_delivered_enq':page_obj_delivered_enq,'page_obj_lost_enq':page_obj_lost_enq})
    else:
        data['html_form'] = render_to_string('Salesperson_Dashboard/salesenq_delete.htm', {'obj_delete':obj_delete}, request=request)
    return JsonResponse(data)





def salesenquiry_search(request):
    try:
        qur = request.GET.get('search')
        page_obj = Enquiry.objects.filter(Q(Name__icontains=qur) | Q(Enquiry_number__icontains=qur) | Q(State__icontains=qur) )
        return render(request,'Salesperson_Dashboard/salesperson.htm',{"page_obj":page_obj})
    except:
        return HttpResponse("please Cannot use None as a query value")




def csv_Files_import(request):
    if request.method == "POST" and request.FILES['file']:
        myfile = request.FILES['file']
        print(myfile)
        fs = FileSystemStorage()
        filename = fs.save(myfile.name,myfile)
        print(filename)
        uploaded_file_url = os.path.join(settings.BASE_DIR+fs.url(filename))

        if os.path.exists(uploaded_file_url) == True:
            print(uploaded_file_url)
            if not  myfile.name.endswith('.csv'):
                messages.error(request,"this is not csv file ") 
            
            with open(uploaded_file_url,'r') as f:
                reader = csv.reader(f)
                print(f)
                # print(reader)
                for column, row in enumerate(reader):
                    if column == 0:
                        pass
                    else:
                        row = "".join(row)
                        row = row.replace(";"," ")
                        row = row.split()
                        print(row)
                        user = User.objects.get(username=row[0])
                        Enq_source = Enquiry_Source.objects.get(enq_source=row[9])
                        profession = Profession.objects.get(profession=row[11])
                        Visit_status = Client_Visit.objects.get(Visit_status=row[12])
                        Enq_number = row[1]
                        mobile_number = row[2]
                        if Enquiry.objects.filter(Enquiry_number=Enq_number).exists():
                            return HttpResponse(f" enquiry number {Enq_number}  alerady existst")
                        elif Enquiry.objects.filter(Contact_number=mobile_number).exists():
                            return HttpResponse(f" mobile  number {mobile_number} alerady existst")
                        else:
                            Enquiry.objects.create(
                                username = user,
                                Enquiry_number = row[1],
                                Contact_number=row[2],
                                Email=row[3],
                                Name=row[4],
                                Company_name=row[5],
                                Enquiry_details=row[6],
                                City=row[7],
                                State=row[8],
                                enquiry_source=Enq_source,
                                expected_purchase_Date=row[10],
                                profession=profession,
                                Visit_status = Visit_status,
                                remarks = row[13]
                            )
            return HttpResponse(" Your csv  File is import successfully ")

    else:
        return redirect("Admin_panel")




    