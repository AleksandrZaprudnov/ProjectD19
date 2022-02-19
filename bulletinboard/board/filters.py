from django_filters import FilterSet, ModelChoiceFilter
from django.forms import BaseModelFormSet, modelformset_factory
from .models import Ad, RespOnAd


class BaseAdFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Ad.objects.filter(name__startswith='0')


class NewsFilterByAd(FilterSet):

    ad_objects = ModelChoiceFilter(field_name='ad', queryset=Ad.objects.all(), label='Объявление')
    # ad_objects = ModelChoiceFilter(field_name='ad', queryset=Ad.objects.all(), label='Объявление')

    class Meta:

        model = RespOnAd

        fields = ['ad_objects']

