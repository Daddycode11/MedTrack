import django_filters
from .models import DetentionInstance, DetentionStatus, DetentionReason, HealthCondition

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
    health_condition = django_filters.ChoiceFilter(
        choices=[('', '---------')] + HealthCondition.CONDITION_CHOICES,
        field_name='pdl_profile__health_conditions__condition',
        label="Condition Type",
    )
    health_status = django_filters.ChoiceFilter(
        choices=[('', '---------')] + HealthCondition.STATUS_CHOICES,
        field_name='pdl_profile__health_conditions__status',
        label="Health Status",
    )

    class Meta:
        model = DetentionInstance
        fields = ['pdl_profile', 'detention_status', 'detention_reason', 'health_condition', 'health_status']
