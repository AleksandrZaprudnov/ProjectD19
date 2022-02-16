from django.contrib import admin
from .models import User, Category, Ad, AdCategory, MediaContent, RespOnAd


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Ad)
admin.site.register(AdCategory)
admin.site.register(MediaContent)
admin.site.register(RespOnAd)
