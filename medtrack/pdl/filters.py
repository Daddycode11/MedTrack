import django_filters
from .models import DetentionInstance, DetentionStatus, DetentionReason

class PDLFilter(django_filters.FilterSet):
    pdl_profile = django_filters.CharFilter(
        field_name='pdl_profile__username__username',
        lookup_expr='icontains',
        label="Name"
    )
    detention_status = django_filters.ModelChoiceFilter(
        queryset=DetentionStatus.objects.all(),
        label="Status"
    )
    detention_reason = django_filters.ModelChoiceFilter(
        queryset=DetentionReason.objects.all(),
        label="Reason"
    )

    class Meta:
        model = DetentionInstance
        fields = ['pdl_profile', 'detention_status', 'detention_reason']