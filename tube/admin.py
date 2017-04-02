from django.contrib import admin
from .models import Video, Category, User
# Register your models here.
admin.site.register(Video)
admin.site.register(Category)
admin.site.register(User)