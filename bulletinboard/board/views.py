from datetime import datetime

from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.views import View
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, DeleteView, ListView
from django.contrib.auth.models import User as UserDjango

from bulletinboard.functions import get_env

from .models import User, Ad, RespOnAd
from .forms import AdModelCreateForm, AdModelUpdateForm, AdResponseForm, \
    RespOnAdModelCreateForm, MediaContentModelCreateForm
from .filters import NewsFilterByAd
from .tasks import send_mail


# Главная страница
class HomePageView(TemplateView):
    template_name = 'home.html'


# Создание объявления
class AdCreateView(CreateView):
    template_name = 'board/ad_create.html'
    form_class = AdModelCreateForm

    def get_form_kwargs(self):
        kwargs = super(AdCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs


# Редактирование объявления
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


# View для GET
# Вывод деталей объявления для просмотра
class AdDetailView(DetailView):
    template_name = 'board/ad_detail.html'
    model = Ad
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super(AdDetailView, self).get_context_data()
        ad = context['ad']

        # Если автор объявления, тогда видит все отклики
        if ad.user.pk == self.request.user.pk:
            resps = RespOnAd.objects.filter(ad_id=ad.pk)
            context['author'] = True
        else:
            resps = RespOnAd.objects.filter(ad_id=ad.pk, user_id=self.request.user.pk)
            context['author'] = False

        context['resps'] = resps
        context['form'] = AdResponseForm()

        return context


# View для POST
# Обработка отклика на объявление
class AdResponseFormView(SingleObjectMixin, FormView):
    template_name = 'books/ad_detail.html'
    form_class = AdResponseForm
    model = Ad

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.get_object()

        user = User.objects.get(user_django=request.user)
        resp = RespOnAd.objects.create(
            user=user,
            ad=self.object,
            text_response=request.POST.__getitem__('text_response')
        )
        resp.save()

        email_from = UserDjango.objects.get(pk=request.user.pk).email

        email_list = [
            UserDjango.objects.get(pk=resp.ad.user.pk).email
        ]

        html_content = render_to_string(
            'board/respone_mail.html',
            {
                'text_title': resp.ad.title,
                'date_time': f'Дата публикации: {resp.datetime_created.strftime("%d/%m/%y %H:%M")}',
                'text_body': f'Сообщение: "{resp.text_response}"',
                'text_contacts': f'Электронная почта: {email_from}',
            }
        )

        email_hu = get_env('EMAIL_HOST_USER')
        subject = f'Объявление "{str(resp.ad)[:30]}", отклик в {datetime.utcnow().strftime("%d/%m/%y %H:%M")}'

        send_mail.apply_async([email_hu, email_list, subject, html_content])
        # send_mail(email_hu, email_list, subject, html_content)

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('ad_detail', kwargs={'pk': self.object.pk})


# Список объявлений
class AdListView(ListView):
    template_name = 'board/ads_list.html'
    model = Ad
    context_object_name = 'ads'
    queryset = Ad.objects.order_by('-datetime_created')


# Создание отклика
class RespOnAdCreateView(CreateView):
    template_name = 'board/responad_create.html'
    form_class = RespOnAdModelCreateForm


# Детали отклика
class RespOnAdDetailView(DetailView):
    template_name = 'board/responad_detail.html'
    model = RespOnAd
    context_object_name = 'responad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Пользователь Django
        author_ad = UserDjango.objects.get(pk=self.object.ad.user.pk)
        # Представление пользователя из профиля
        author_pd = self.object.ad.user
        email_from = author_ad.email

        context['text_title'] = self.object.ad.title
        context['date_time'] = f'Дата публикации: {self.object.datetime_created.strftime("%d/%m/%y %H:%M")}'
        context['text_body'] = f'{self.object.text_response}'
        context['text_contacts'] = f'Имя: {author_pd}; эл. почта: {email_from}'

        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.get_object()

        # Пользователь Django
        author_ad = request.user
        # Представление пользователя из профиля
        author_pd = self.object.ad.user
        email_from = author_ad.email

        email_list = [
            UserDjango.objects.get(pk=self.object.user.pk).email
        ]

        html_content = render_to_string(
            'board/respone_mail.html',
            {
                'text_title': self.object.ad.title,
                'date_time': f'Дата публикации: {self.object.datetime_created.strftime("%d/%m/%y %H:%M")}',
                'text_body': f'Вы писали: "{self.object.text_response}"',
                'text_contacts': f'имя: {author_pd}; эл. почта: {email_from}',
            }
        )

        email_hu = get_env('EMAIL_HOST_USER')
        subject = f'Принят отклик к объявлению "{str(self.object.ad)[:30]}", в {datetime.utcnow().strftime("%d/%m/%y %H:%M")}'

        send_mail.apply_async([email_hu, email_list, subject, html_content])
        # send_mail(email_hu, email_list, subject, html_content)

        return super().get(request, *args, **kwargs)


# Обработка GET и POST запросов объявления
class AdView(View):

    def get(self, request, *args, **kwargs):
        view = AdDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AdResponseFormView.as_view()
        return view(request, *args, **kwargs)


# Удаление отклика
class RespOnAdDeleteView(DeleteView):
    template_name = 'board/responad_delete.html'
    queryset = RespOnAd.objects.all()

    def get_success_url(self):
        return reverse('ad_update', kwargs={'pk': self.object.ad.id})


class RespOnAdListView(ListView):
    template_name = 'board/responad_list.html'
    model = RespOnAd
    context_object_name = 'resps'
    ordering = '-datetime_created'
    paginate_by = 1

    def get_queryset(self, **kwargs):

        if not self.request.user.is_authenticated:
            qs = RespOnAd.objects.none()
        else:
            user = User.objects.get(user_django=self.request.user)
            qs = RespOnAd.objects.filter(ad__user__id=user.pk)

        return qs

    def get_context_data(self, **kwargs):
        context = super(RespOnAdListView, self).get_context_data()

        filtered = NewsFilterByAd(self.request.GET, request=self.get_queryset())

        if self.request.user.is_authenticated:
            user = User.objects.get(user_django=self.request.user)
            ad_qs = Ad.objects.filter(user=user)
            filtered.qs.filter(ad__in=ad_qs)

        context['filter'] = filtered

        person_page_object = None
        if filtered.qs.count():
            # pass
            paginated_filtered_persons = Paginator(filtered.qs, self.paginate_by)
            page_number = self.request.GET.get('page')
            person_page_object = paginated_filtered_persons.get_page(page_number)

        context['person_page_object'] = person_page_object
        # context['signed'] = self.signed

        return context


# Добавление файлов
class MediaContentCreateView(CreateView):
    template_name = 'board/file_upload.html'
    form_class = MediaContentModelCreateForm

    def get_form_kwargs(self):
        kwargs = super(MediaContentCreateView, self).get_form_kwargs()
        kwargs['name_file'] = str(self.request.user.pk) + '_mc_' + datetime.utcnow().strftime("%d%m%y%H%M%S")
        return kwargs

    def get_success_url(self):
        return reverse('mediacontent_create')

