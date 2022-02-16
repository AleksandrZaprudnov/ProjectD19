import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Ad, RespOnAd
from .forms import AdModelCreateForm, AdModelUpdateForm, AdResponseForm


class HomePageView(TemplateView):
    template_name = 'home.html'


class AdCreateView(CreateView):
    template_name = 'board/ad_create.html'
    form_class = AdModelCreateForm

    def get_form_kwargs(self):
        kwargs = super(AdCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class AdUpdateView(UpdateView):
    template_name = 'board/ad_update.html'
    form_class = AdModelUpdateForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Ad.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super(AdUpdateView, self).get_context_data(**kwargs)
        ad = context['ad']
        resps = RespOnAd.objects.filter(ad_id=ad.pk)
        context['resps'] = resps

        return context


class AdDetailView(DetailView):
    template_name = 'board/ad_detail.html'
    model = Ad
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super(AdDetailView, self).get_context_data(**kwargs)
        ad = context['ad']
        resps = RespOnAd.objects.filter(ad_id=ad.pk)
        context['resps'] = resps
        print(resps)
        context['form'] = AdResponseForm().get_context()
        print(context['form'])
        print(AdResponseForm())

        return context


class AdListView(ListView):
    template_name = 'board/ads_list.html'
    model = Ad
    context_object_name = 'ads'
    queryset = Ad.objects.order_by('-datetime_created')


class AdResponseFormView(SingleObjectMixin, FormView):
    pass
#     template_name = 'board/ad_detail.html'
#     form_class = AdResponseForm
#     model = Ad
#
#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()
#         self.object = self.get_object()
#         return super().post(request, *args, **kwargs)
#
#     def get_success_url(self):
#         return reverse('ad_detail', kwargs={'pk': self.object.pk})


class AdView(View):
    pass
#
#     def get(self, request, *args, **kwargs):
#         view = AdDetailView.as_view()
#         return view(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         view = AdResponseFormView.as_view()
#         return view(request, *args, **kwargs)

