# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profileheading = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    freelance = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='profile/images', default='img/profile.png')
    address = models.CharField(max_length=500, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    mobile = models.CharField(max_length=12, blank=True, null=True)
    # Payment Integration
    razorpay = models.CharField(max_length=200, blank=True, null=True)
    paypal = models.CharField(max_length=200, blank=True, null=True)
    # Social Media
    facebook = models.CharField(max_length=200, blank=True, null=True)
    twitter = models.CharField(max_length=200, blank=True, null=True)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    youtube = models.CharField(max_length=200, blank=True, null=True)
    pinterest = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.user.first_name} Profile'

    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)
    #
    #     img = Image.open(self.profile_pic.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.profile_pic.path)


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='image_user')
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(max_length=1000, blank=True, null=True)
    file_uploaded = models.FileField(upload_to='images', blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    views = models.IntegerField(default=0)
    total_downloads = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, default=None, blank=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return self.title

    @property
    def number_of_liked(self):
        return self.likes.count()


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(max_length=1000, blank=True, null=True)
    file_uploaded = models.FileField(upload_to='videos', blank=False)
    tags = TaggableManager()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Music(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(max_length=1000, blank=True, null=True)
    file_uploaded = models.FileField(upload_to='musics', blank=False)
    tags = TaggableManager()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
