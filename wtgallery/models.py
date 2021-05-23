# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager
from PIL import Image
from django.conf import settings
from django.utils.text import slugify
import re


class Ranks(models.Model):
    name = models.CharField(max_length=20)
    followers = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Ranks"


# TODO: Add followers field for each user
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profileheading = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    freelance = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    ranks = models.ManyToManyField(Ranks, blank=True)
    profile_pic = models.ImageField(upload_to='profile/images', default='img/profile.png')
    address = models.CharField(max_length=500, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=15, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    # Payment Integration
    razorpay = models.CharField(max_length=200, blank=True, null=True)
    paypal = models.CharField(max_length=20, blank=True, null=True)
    upi = models.CharField(max_length=20, blank=True, null=True)
    # Social Media
    facebook = models.CharField(max_length=200, blank=True, null=True)
    twitter = models.CharField(max_length=200, blank=True, null=True)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    youtube = models.CharField(max_length=200, blank=True, null=True)
    pinterest = models.CharField(max_length=200, blank=True, null=True)
    # Followers & Following
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    following = models.ManyToManyField(User, blank=True, related_name='following')

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        db_table = 'Profiles'

    def __str__(self):
        return f'{self.user.first_name}'

    @property
    def number_of_followers(self):
        return self.followers.count()

    @property
    def number_of_following(self):
        return self.following.count()


STATUS = (
    ("A", "Approved"),
    ("P", "Pending"),
    ("R", "Reject"),
)


class Image(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='image_user')
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(max_length=1000, blank=True, null=True)
    file = models.ImageField(upload_to='images', blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    views = models.IntegerField(default=0)
    total_downloads = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, default=None, blank=True)
    status = models.CharField(max_length=1, default='P', choices=STATUS)
    slug = models.SlugField(max_length=80, unique=True)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete(save=False)
        super().delete(*args, **kwargs)

    @property
    def number_of_likes(self):
        return self.likes.count()


class Video(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(max_length=1000, blank=True, null=True)
    file = models.FileField(upload_to='videos', blank=False)
    tags = TaggableManager()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    total_downloads = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, default=None, blank=True)
    status = models.CharField(max_length=1, default='P', choices=STATUS)
    slug = models.SlugField(max_length=80, unique=True)

    class Meta:
        verbose_name = 'video'
        verbose_name_plural = 'videos'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete(save=False)
        super().delete(*args, **kwargs)


class Music(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(max_length=1000, blank=True, null=True)
    file = models.FileField(upload_to='musics', blank=False)
    thumbnail = models.ImageField(upload_to='musics/thumbnails', default='img/9.jpg')
    tags = TaggableManager()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    total_downloads = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, default=None, blank=True)
    status = models.CharField(max_length=1, default='P', choices=STATUS)
    slug = models.SlugField(max_length=80, unique=True)

    class Meta:
        verbose_name = 'Music'
        verbose_name_plural = 'Music'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete(save=False)
        self.thumbnail.delete(save=False)
        super().delete(*args, **kwargs)
