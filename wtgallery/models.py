# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager
from PIL import Image


# TODO: Add followers field for each user
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profileheading = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    freelance = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='profile/images', default='img/profile.png')
    address = models.CharField(max_length=500, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.PositiveIntegerField(blank=True, null=True)
    mobile = models.PositiveIntegerField(blank=True, null=True)
    # Payment Integration
    razorpay = models.CharField(max_length=200, blank=True, null=True)
    paypal = models.CharField(max_length=200, blank=True, null=True)
    upi = models.CharField(max_length=20, blank=True, null=True)
    # Social Media
    facebook = models.CharField(max_length=200, blank=True, null=True)
    twitter = models.CharField(max_length=200, blank=True, null=True)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    youtube = models.CharField(max_length=200, blank=True, null=True)
    pinterest = models.CharField(max_length=200, blank=True, null=True)

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

    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)
    #
    #     img = Image.open(self.profile_pic.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.profile_pic.path)


# Need Not to register on admin
class UserFollowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    follows = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        verbose_name = "Following"

    def get_followers(self):
        return self.objects.filter(follows=self.user).count()

    def get_following(self):
        return self.objects.filter(user=self.user).count()


STATUS = (
    ("A", "Approved"),
    ("P", "Pending"),
    ("R", "Reject"),
)


class Image(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='image_user')
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(max_length=1000, blank=True, null=True)
    file = models.FileField(upload_to='images', blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    views = models.IntegerField(default=0)
    total_downloads = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, default=None, blank=True)
    status = models.CharField(max_length=1, default='P', choices=STATUS)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return self.title

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

    class Meta:
        verbose_name = 'video'
        verbose_name_plural = 'videos'

    def __str__(self):
        return self.title


class Music(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(max_length=1000, blank=True, null=True)
    file = models.FileField(upload_to='musics', blank=False)
    tags = TaggableManager()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    total_downloads = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, default=None, blank=True)
    status = models.CharField(max_length=1, default='P', choices=STATUS)

    class Meta:
        verbose_name = 'Music'
        verbose_name_plural = 'Music'

    def __str__(self):
        return self.title
