from .models import Enquiry
import django_filters


class EnquiryFilter(django_filters.FilterSet):
    class Meta:
        model = Enquiry
        fields = ['Enquiry_number', 'Name', 'Visit_status', ]
