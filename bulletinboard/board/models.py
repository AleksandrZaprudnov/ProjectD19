import requests
from django.db import models
from django.contrib.auth.models import User as UserDjango
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


# Модель User (Пользователь)
# Модель, содержащая всех пользователей
# Имеет поля:
# name - имя пользователя
# user_django - связь один к одному с пользователем Django,
#   для создания пользователей при регистрации
# - имя пользователя.

class User(models.Model):
    name = models.CharField(max_length=255, null=False)
    user_django = models.OneToOneField(UserDjango, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name.title()}'

    @receiver(post_save, sender=UserDjango)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            user = User.objects.create(user_django=instance)
            user.name = instance.username
            user.save()

    @receiver(post_save, sender=UserDjango)
    def save_user_profile(sender, instance, **kwargs):
        pass


# Модель Category
# Категории объявлений,
# Имеет единственное поле: название категории.
# Поле должно быть уникальным.

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return f'{self.name.title()}'


# Модель MediaContent
# Эта модель содержит файлы, загружаемые пользователем.
# Соответственно, модель должна включать следующие поля:
# связь «один ко многим» с моделью Ad;
# имя файла;
# ссылка на файл в директории проекта.

class MediaContent(models.Model):
    ad = models.ForeignKey("Ad", on_delete=models.CASCADE, related_name="files")
    name_file = models.CharField(max_length=20, unique=True, null=False)
    link_file = models.FileField(upload_to='media')

    def __str__(self):
        return f'{self.name_file}'


# Модель Response
# Эта модель содержит отклики/комментарии, оставленные пользователями к объявлениям.
# Соответственно, модель должна включать следующие поля:
# связь «один ко многим» с моделью Ad;
# связь «один ко многим» с моделью User;
# текст отклика.

class RespOnAd(models.Model):
    ad = models.ForeignKey("Ad", on_delete=models.CASCADE, related_name="responad")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="responad")
    text_response = models.TextField(null=False)
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.text_response[:15]}'

    def get_absolute_url(self):
        return f'/responad_detail/{self.id}'


# Модель Ad
# Эта модель содержит объявления и новости,
# которые создают зарегистрированные пользователи.
# Каждый объект может иметь одну или несколько категорий.
# Соответственно, модель должна включать следующие поля:
# связь «один ко многим» с моделью User;
# поле-признак - «Новость»;
# автоматически добавляемая дата и время создания;
# связь «многие ко многим» с моделью Category (с дополнительной моделью AdCategory);
# заголовок статьи/новости;
# текст статьи/новости.


class Ad(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="ads")
    type_ad_news = models.BooleanField(default=False)
    datetime_created = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField("Category", through="AdCategory")
    title = models.CharField(max_length=255, null=False)
    text_article = models.TextField(null=False)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f'/board/ad_detail/{self.id}'


# Модель AdCategory
# Промежуточная модель для связи «многие ко многим»:
# связь «один ко многим» с моделью Ad;
# связь «один ко многим» с моделью Category.

class AdCategory(models.Model):
    ads = models.ForeignKey("Ad", on_delete=models.CASCADE)
    categories = models.ForeignKey("Category", on_delete=models.CASCADE)

