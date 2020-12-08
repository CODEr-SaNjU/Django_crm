from django.contrib import admin
from .models import Enquiry ,Profession,Client_Visit,Enquiry_Source,visit_status_time



admin.site.register(Profession)
admin.site.register(Client_Visit)
admin.site.register(Enquiry_Source)
admin.site.register(Enquiry)
admin.site.register(visit_status_time)