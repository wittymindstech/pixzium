from django.contrib import admin

# Register your models here.
from wtgallery.models import Music, Image, Video, Profile

admin.site.register(Profile)

admin.site.register(Image)

admin.site.register(Video)

admin.site.register(Music)
