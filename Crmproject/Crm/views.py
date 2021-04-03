from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth, Group
from django.http import Http404, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib import messages
import csv
import io
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, get_user_model
from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from . decorators import unauthenticated_user, allowed_user, admin_only
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
import os
from django.http import JsonResponse
from . forms import UserForm, SalespersonEnquiryForm, CreateEnquiryForm, UpdateEnquiryForm, salespersonUpdateEnquiryForm, salespersonstatusEnquiryForm
import requests
from django.db.models import Q
import json
from django.conf import settings
from django.urls import reverse_lazy
from .models import Enquiry, Enquiry_Source, Profession, Client_Visit, History
from django.template.loader import render_to_string
import datetime
import pytz


@unauthenticated_user
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('Admin_panel')
        else:
            messages.error(
                request, 'Error! please enter the correct  username and Password for a staff account.')
            return render(request, 'html_files/login.htm')
    else:
        return render(request, "html_files/login.htm")


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
            messages.success(
                request, f'Registration complete! You may log in!')
    else:
        userform = UserForm(request.POST)
    all_user = User.objects.all()  # return all user here

    all_enq = Enquiry.objects.all().order_by('id')
    paginator = Paginator(all_enq, 10)
    page_number = request.GET.get('page')
    page_obj_all_enq = paginator.get_page(page_number)
    total_enquiry_data = all_enq.count()

    assign_enq = Enquiry.objects.filter(username__isnull=False).order_by('id')
    paginator = Paginator(assign_enq, 10)
    page_number = request.GET.get('page')
    page_obj_assign_enq = paginator.get_page(page_number)
    assign_enq_count = assign_enq.count()

    notassign_enq = Enquiry.objects.filter(
        username__isnull=True).order_by('id')
    paginator = Paginator(notassign_enq, 10)
    page_number = request.GET.get('page')
    page_obj_notassign_enq = paginator.get_page(page_number)
    notassign_enq_count = notassign_enq.count()
    last_all_enq = Enquiry.objects.filter().order_by('-id')[:14]
    all_enq_in_ascending_order = reversed(last_all_enq)

    return render(request, 'html_files/Dashboard.htm', {'last_all_enq': last_all_enq, 'total_enquiry_data': total_enquiry_data, 'page_obj_all_enq': page_obj_all_enq, 'userform': userform, 'all_user': all_user, 'page_obj_assign_enq': page_obj_assign_enq, 'page_obj_notassign_enq': page_obj_notassign_enq, 'assign_enq_count': assign_enq_count, 'notassign_enq_count': notassign_enq_count})


@login_required(login_url='login')
def search_enq_month(request):
    try:
        qur = request.GET.get('search')
        qur1 = request.GET.get("search1")
        last_all_enq = Enquiry.objects.filter(Created_at__range=(qur, qur1))
        return render(request, 'html_files/Dashboard.htm', {"last_all_enq": last_all_enq})
    except:
        return redirect('Admin_panel')


@login_required(login_url='login')
@admin_only
def Enquiry_search(request):
    ctx = {}
    url_parameter = request.GET.get('q')
    if url_parameter:
        last_all_enq = Enquiry.objects.filter(Q(Name__icontains=url_parameter) | Q(
            Enquiry_number__icontains=url_parameter) | Q(State__icontains=url_parameter))
    else:
        last_all_enq = Enquiry.objects.all()

    ctx["last_all_enq"] = last_all_enq
    if request.is_ajax():
        html = render_to_string(
            template_name='html_files/enq_list.htm', context={"last_all_enq": last_all_enq})
        print("line number 114", html)
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)
    return render(request, "html_files/Dashboard.htm", context=ctx)


@login_required(login_url='login')
def save_enq_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            rmrks = user.Remarks
            Enquiry_number = user
            vist_status = user.Enquiry_status
            user = user.username
            History.objects.create(
                update_by=user, Enquiry_number=Enquiry_number, Enquiry_status=vist_status, Remarks=rmrks)
            data['form_is_valid'] = True
            last_all_enq = Enquiry.objects.filter().order_by('-id')[:10]
            data['html_enq_list'] = render_to_string(
                'html_files/enq_list.htm', {'last_all_enq': last_all_enq})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)


@login_required(login_url='login')
def validate_Number(request):
    '''Check contact number availability'''
    Contact_number = request.GET.get('Contact_number', None)
    response = {
        'is_taken': Enquiry.objects.filter(Contact_number__iexact=Contact_number).exists()
    }
    return JsonResponse(response)


@login_required(login_url='login')
def history_view(request, pk_id):
    data = dict()
    enq = Enquiry.objects.get(id=pk_id)
    application_detail = History.objects.filter(Enquiry_number=enq)
    data['html_form'] = render_to_string(
        'html_files/history.htm', {"application_detail": application_detail}, request=request)
    return JsonResponse(data)


@login_required(login_url='login')
def enq_create(request):
    data = dict()
    if request.method == 'POST':
        form = CreateEnquiryForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            Enquiry_number = user
            Enquiry_status = user.Enquiry_status
            user = user.username
            History.objects.create(
                update_by=user, Enquiry_number=Enquiry_number, Enquiry_status=Enquiry_status,)
            data['form_is_valid'] = True
            last_all_enq = Enquiry.objects.all()
            data['html_enq_list'] = render_to_string(
                'html_files/enq_list.htm', {'last_all_enq': last_all_enq})
        else:
            data['form_is_valid'] = False
    else:
        form = CreateEnquiryForm()
    context = {'form': form}
    data['html_form'] = render_to_string(
        'html_files/add_enq.htm', context, request=request)
    return JsonResponse(data)


@login_required(login_url='login')
def Enquiry_Update(request, pk_id):
    obj_update = get_object_or_404(Enquiry, id=pk_id)
    if request.method == "POST":
        form = UpdateEnquiryForm(request.POST, instance=obj_update)
    else:
        form = UpdateEnquiryForm(instance=obj_update)
    return save_enq_form(request, form, 'html_files/enquiry_update.htm')


@login_required(login_url='login')
def Enquiry_Delete(request, pk_id):
    obj_delete = get_object_or_404(Enquiry, id=pk_id)
    data = dict()
    if request.method == "POST":
        obj_delete.delete()
        data['form_is_valid'] = True
        last_all_enq = Enquiry.objects.filter().order_by('-id')[:10]
        data['html_enq_list'] = render_to_string(
            'html_files/enq_list.htm', {'last_all_enq': last_all_enq})
    else:
        data['html_form'] = render_to_string(
            'html_files/enquiry_delete.htm', {'obj_delete': obj_delete}, request=request)
    return JsonResponse(data)


@login_required(login_url='login')
def save_user_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            all_user = User.objects.all()
            data['html_user_list'] = render_to_string(
                'html_files/all_user_list.htm', {'all_user': all_user})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)


@login_required(login_url='login')
def user_update(request, pk_id):
    user_update = get_object_or_404(User, id=pk_id)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user_update)
    else:
        form = UserForm(instance=user_update)
    return save_user_form(request, form, 'html_files/user_update.htm')


@login_required(login_url='login')
def user_delete(request, pk_id):
    user_delete = get_object_or_404(User, id=pk_id)
    data = dict()
    if request.method == "POST":
        user_delete.delete()
        data['form_is_valid'] = True
        all_user = User.objects.all()
        data['html_user_list'] = render_to_string(
            'html_files/all_user_list.htm', {'all_user': all_user})
    else:
        data['html_form'] = render_to_string(
            'html_files/user_delete.htm', {'user_delete': user_delete}, request=request)
    return JsonResponse(data)


@login_required(login_url='login')
def saleperson_page(request):
    ctx = {}
    url_parameter = request.GET.get("q")
    if url_parameter:
        page_obj_cold_enq = Enquiry.objects.filter(Q(Name__icontains=url_parameter) | Q(
            Enquiry_number__icontains=url_parameter) | Q(State__icontains=url_parameter), username=request.user)
    else:
        all_enq = Enquiry.objects.all()
        Hot_enq = Enquiry.objects.filter(
            Enquiry_status__Enquiry_status__icontains="Hot", username=request.user).order_by('id')
        paginator = Paginator(Hot_enq, 14)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        Hot_enq_count = Hot_enq.count()

        cold_enq = Enquiry.objects.filter(
            username=request.user, Enquiry_status__Enquiry_status__icontains="COLD").order_by('id')
        paginator = Paginator(cold_enq, 14)
        page_number = request.GET.get('page')
        page_obj_cold_enq = paginator.get_page(page_number)
        cold_enq_count = cold_enq.count()

        pending_enq = Enquiry.objects.filter(
            username=request.user, Enquiry_status__Enquiry_status__icontains="Pending").order_by('id')
        paginator = Paginator(pending_enq, 14)
        page_number = request.GET.get('page')
        page_obj_pending_enq = paginator.get_page(page_number)
        pending_enq_count = pending_enq.count()

        delivered_enq = Enquiry.objects.filter(
            username=request.user, Enquiry_status__Enquiry_status__icontains="Delivered").order_by('id')
        paginator = Paginator(delivered_enq, 14)
        page_number = request.GET.get('page')
        page_obj_delivered_enq = paginator.get_page(page_number)
        delivered_enq_count = delivered_enq.count()

        # today follow up code
        today_follow_up_enq = Enquiry.objects.filter(
            username=request.user, Enquiry_status__Enquiry_status__icontains="Follow up", Follow_up=datetime.datetime.today()).order_by('id')
        paginator = Paginator(today_follow_up_enq, 14)
        page_number = request.GET.get('page')
        page_obj_today_follow_up_enq = paginator.get_page(page_number)
        today_follow_up_enq_count = today_follow_up_enq.count()

        # future follow up
        follow_up_enq = Enquiry.objects.filter(username=request.user, Enquiry_status__Enquiry_status__icontains="Follow up",
                                               Follow_up__gte=datetime.datetime.today()+datetime.timedelta(days=1)).order_by('id')
        paginator = Paginator(follow_up_enq, 14)
        page_number = request.GET.get('page')
        page_obj_follow_up_enq = paginator.get_page(page_number)
        follow_up_enq_count = follow_up_enq.count()

        lost_enq = Enquiry.objects.filter(
            username=request.user, Enquiry_status__Enquiry_status__icontains='Lost').order_by('id')
        paginator = Paginator(lost_enq, 14)
        page_number = request.GET.get('page')
        page_obj_lost_enq = paginator.get_page(page_number)
        lost_enq_count = lost_enq.count()

    ctx["page_obj_cold_enq"] = page_obj_cold_enq
    if request.is_ajax():
        html = render_to_string(
            template_name="Salesperson_Dashboard/cold_list.htm",
            context={
                "page_obj_cold_enq": page_obj_cold_enq}
        )
        print("line number 328", html)
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    return render(request, 'Salesperson_Dashboard/salesperson_dashboard.htm', context=ctx)


@login_required(login_url='login')
def salesperson_save_enq_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            page_obj_cold_enq = Enquiry.objects.filter(
                username=request.user, Enquiry_status__Enquiry_status__icontains="cold")
            page_obj = Enquiry.objects.filter(
                Enquiry_status__Enquiry_status__icontains='Hot', username=request.user)
            page_obj_pending_enq = Enquiry.objects.filter(
                username=request.user, Enquiry_status__Enquiry_status__icontains='Pending')
            page_obj_delivered_enq = Enquiry.objects.filter(
                username=request.user, Enquiry_status__Enquiry_status__icontains="Delivered")
            page_obj_lost_enq = Enquiry.objects.filter(
                username=request.user, Enquiry_status__Enquiry_status__icontains="Lost")
            data['html_enq_list'] = render_to_string('Salesperson_Dashboard/cold_list.htm', {'page_obj_cold_enq': page_obj_cold_enq, 'page_obj': page_obj,
                                                                                             'page_obj_pending_enq': page_obj_pending_enq, 'page_obj_delivered_enq': page_obj_delivered_enq, 'page_obj_lost_enq': page_obj_lost_enq})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)


@login_required(login_url='login')
def salesperson_enq_create(request):
    data = dict()
    if request.method == 'POST':
        form = SalespersonEnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.username = request.user
            enquiry.save()
            Enquiry_number = enquiry  # enq number
            user = form.save()
            user.username = request.user
            vist_status = user.Enquiry_status
            user = user.username
            History.objects.create(
                update_by=user, Enquiry_number=Enquiry_number, Enquiry_status=vist_status,)
            data['form_is_valid'] = True
            page_obj_cold_enq = Enquiry.objects.filter(
                username=request.user, Enquiry_status__Enquiry_status__icontains="Hot")
            page_obj = Enquiry.objects.filter(
                Enquiry_status__Enquiry_status__icontains='Cold', username=request.user)
            page_obj_pending_enq = Enquiry.objects.filter(
                username=request.user, Enquiry_status__Enquiry_status__icontains='Pending')
            page_obj_delivered_enq = Enquiry.objects.filter(
                username=request.user, Enquiry_status__Enquiry_status__icontains='Delivered')
            page_obj_lost_enq = Enquiry.objects.filter(
                username=request.user, Enquiry_status__Enquiry_status__icontains='Lost')
            data['html_enq_list'] = render_to_string('Salesperson_Dashboard/cold_list.htm', {'page_obj_cold_enq': page_obj_cold_enq, 'page_obj': page_obj,
                                                                                             'page_obj_pending_enq': page_obj_pending_enq, 'page_obj_delivered_enq': page_obj_delivered_enq, 'page_obj_lost_enq': page_obj_lost_enq})
        else:
            data['form_is_valid'] = False
    else:
        form = SalespersonEnquiryForm()
    context = {'form': form}
    data['html_form'] = render_to_string(
        'Salesperson_Dashboard/add_enq.htm', context, request=request)
    return JsonResponse(data)


@login_required(login_url='login')
def salesperson_Enquiry_Update(request, pk_id):
    obj_update = get_object_or_404(Enquiry, id=pk_id)
    if request.method == "POST":
        form = salespersonUpdateEnquiryForm(request.POST, instance=obj_update)
    else:
        form = salespersonUpdateEnquiryForm(instance=obj_update)
    return salesperson_save_enq_form(request, form, 'Salesperson_Dashboard/salesenq_update.htm')


@login_required(login_url='login')
@login_required(login_url='login')
def salesperson_Enquiry_Delete(request, pk_id):
    obj_delete = get_object_or_404(Enquiry, id=pk_id)
    data = dict()
    if request.method == "POST":
        obj_delete.delete()
        data['form_is_valid'] = True
        page_obj_cold_enq = Enquiry.objects.filter(
            username=request.user, Enquiry_status__Enquiry_status__icontains='COLD')
        page_obj = Enquiry.objects.filter(
            Enquiry_status__Enquiry_status__icontains='Hot', username=request.user)
        page_obj_pending_enq = Enquiry.objects.filter(
            username=request.user, Enquiry_status__Enquiry_status__icontains='Pending')
        page_obj_delivered_enq = Enquiry.objects.filter(
            username=request.user, Enquiry_status__Enquiry_status__icontains='Delivered')
        page_obj_lost_enq = Enquiry.objects.filter(
            username=request.user, Enquiry_status__Enquiry_status__icontains='Lost')
        data['html_enq_list'] = render_to_string('Salesperson_Dashboard/cold_list.htm', {'page_obj_cold_enq': page_obj_cold_enq, 'page_obj': page_obj,
                                                                                         'page_obj_pending_enq': page_obj_pending_enq, 'page_obj_delivered_enq': page_obj_delivered_enq, 'page_obj_lost_enq': page_obj_lost_enq})
    else:
        data['html_form'] = render_to_string(
            'Salesperson_Dashboard/salesenq_delete.htm', {'obj_delete': obj_delete}, request=request)
    return JsonResponse(data)


@login_required(login_url='login')
def salesenquiry_reports(request):
    try:
        featured_filter = request.GET.get('filterstatus')
        filterdata = Enquiry.objects.filter(
            Enquiry_status__Enquiry_status__icontains=featured_filter)
        total_filterdata_data = filterdata.count()
        return render(request, 'Salesperson_Dashboard/salesperson_dashboard.htm', {"filterdata": filterdata, "total_filterdata_data": total_filterdata_data})
    except:
        return redirect('saleperson')


@login_required(login_url='login')
def salespersonsearch_enq_month(request):
    try:
        qur = request.GET.get('search')
        qur1 = request.GET.get("search1")
        page_obj = Enquiry.objects.filter(created_at__range=(qur, qur1))
        return render(request, 'Salesperson_Dashboard/salesperson_dashboard.htm', {"page_obj": page_obj})
    except:
        return redirect('saleperson')


@login_required(login_url='login')
def csv_Files_import(request):
    if request.method == "POST" and request.FILES['file']:
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = os.path.join(settings.BASE_DIR+fs.url(filename))

        if os.path.exists(uploaded_file_url) == True:
            if not myfile.name.endswith('.csv'):
                messages.error(request, "this is not csv file ")

            with open(uploaded_file_url, 'r') as f:
                reader = csv.reader(f)
                for column, row in enumerate(reader):
                    if column == 0:
                        pass
                    else:
                        row = "".join(row)
                        row = row.replace(";", " ")
                        row = row.split()
                        user = User.objects.get(username=row[0])
                        Enq_source = Enquiry_Source.objects.get(
                            enq_source=row[9])
                        profession = Profession.objects.get(profession=row[11])
                        Enquiry_status = Client_Visit.objects.get(
                            Enquiry_status=row[12])
                        Enq_number = row[1]
                        mobile_number = row[2]
                        if Enquiry.objects.filter(Enquiry_number=Enq_number).exists():
                            return HttpResponse(f" enquiry number {Enq_number}  alerady existst")
                        elif Enquiry.objects.filter(Contact_number=mobile_number).exists():
                            return HttpResponse(f" mobile  number {mobile_number} alerady existst")
                        else:
                            Enquiry.objects.create(
                                username=user,
                                Enquiry_number=row[1],
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
                                Enquiry_status=Enquiry_status,
                                remarks=row[13]
                            )
            return HttpResponse(" Your csv  File is import successfully ")

    else:
        return redirect("Admin_panel")
