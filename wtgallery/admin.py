import django.contrib.auth.models
from django.contrib import admin

# Register your models here.
from wtgallery.models import Music, Image, Video, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'freelance', 'verified']
    list_editable = ['verified']
    list_filter = ['verified', 'freelance']
    search_fields = ['user__username']
    fieldsets = (
        (None, {
            'fields': ('user', 'profileheading',
                       'description', 'freelance', 'profile_pic')
        }),
        ('Address', {
            'classes': ('collapse',),
            'fields': ('address', 'country', 'state', 'city', 'pincode'),
        }),
        ('Payment Options', {
            'classes': ('collapse',),
            'fields': ('razorpay', 'paypal', 'upi',),
        }),
        ('Social Liks', {
            'classes': ('collapse',),
            'fields': ('facebook', 'twitter', 'instagram', 'youtube', 'pinterest'),
        })
    )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'tags', 'status']
    list_editable = ['tags', 'status']
    list_filter = ('user', 'status',)
    filter_horizontal = ('likes',)
    search_fields = ('tags__name', 'user__user__username', 'title')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'tags', 'status']
    list_editable = ['tags', 'status']
    list_filter = ('user', 'status',)
    filter_horizontal = ('likes',)
    search_fields = ('tags__name', 'user__user__username', 'title')


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'tags', 'status']
    list_editable = ['tags', 'status']
    list_filter = ('user', 'status',)
    filter_horizontal = ('likes',)
    search_fields = ('tags__name', 'user__user__username', 'title')
