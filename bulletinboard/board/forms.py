from django import forms
from django.forms import ModelForm
from .models import Ad, Category, User, RespOnAd, MediaContent


class AdModelCreateForm(ModelForm):
    type_ad_news = forms.BooleanField(required=False, label='Новость')
    title = forms.CharField(label='Заголовок')
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), label='Категории', widget=forms.SelectMultiple)
    text_article = forms.CharField(max_length=500, label='Содержание', widget=forms.Textarea)

    class Meta:
        model = Ad
        fields = '__all__'
        exclude = [
            'user', 'media_content',
        ]

    # Переопределяем инициализацию
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        self.instance.user = User.objects.filter(user_django=self.user).first()
        return super(AdModelCreateForm, self).save(commit=commit)


class AdModelUpdateForm(ModelForm):
    type_ad_news = forms.BooleanField(required=False, label='Новость')
    title = forms.CharField(label='Заголовок')
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), label='Категории', widget=forms.SelectMultiple)
    text_article = forms.CharField(max_length=500, label='Содержание', widget=forms.Textarea)
    link_home_page = forms.CharField(max_length=255, label='Ссылка на файл главной страницы')

    class Meta:
        model = Ad
        fields = '__all__'
        exclude = [
            'user',
        ]


class RespOnAdModelCreateForm(ModelForm):

    class Meta:
        model = RespOnAd
        fields = '__all__'
        # exclude = [
        #     'ad', 'user',
        # ]


class AdResponseForm(forms.Form):
    text_response = forms.CharField(
        max_length=500,
        label='',
        widget=forms.Textarea
    )

    text_response.widget.attrs.update({
        'class': 'form-control',
        'rows': '3',
        'placeholder': 'Оставьте отклик на объявление...',
    })


class RespOnAdModelDetailForm(ModelForm):

    class Meta:
        model = RespOnAd
        fields = '__all__'


class MediaContentModelCreateForm(ModelForm):

    class Meta:
        model = MediaContent
        fields = '__all__'
        exclude = [
            'name_file',
        ]

    # Переопределяем инициализацию
    def __init__(self, name_file, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name_file = name_file

    def save(self, commit=True):
        self.instance.name_file = self.name_file + '_ad_' + str(self.instance.ad.pk)
        return super(MediaContentModelCreateForm, self).save(commit=commit)

