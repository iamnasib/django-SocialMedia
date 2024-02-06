import os
import random
from time import time
from django.db.models.fields.related import ForeignKey
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, Anchor
from PIL import Image
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from datetime import date
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.


def photo_pathh(instance, filename):
    current_dateTime = datetime.now()
    #dt_string = current_dateTime.strftime()
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(10))
    return 'DP/{basename}{username}-{randomstring}{ext}'.format(username=instance.username, basename="DP-", randomstring=current_dateTime, ext=file_extension)


class MyUser(AbstractUser):
    full_name = models.CharField(max_length=200)
    DOB = models.DateField(blank=True, null=True)
    DP = ProcessedImageField(upload_to=photo_pathh, help_text="Profile Picture",
                             default="DP/default.jpg",
                             verbose_name="Profile Picture",
                             processors=[ResizeToFill(170, 170)],
                             format='JPEG',
                             options={'quality': 80})
    bio = models.TextField(blank=True, max_length=300)
    website = models.URLField(blank=True)
    mobile_number = models.CharField(max_length=10, blank=True)
    gender = models.CharField(null=True, blank=True, max_length=8)
    is_deactivated = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_private=models.BooleanField(default=False)
    followers = models.ManyToManyField(
        "self", blank=True, related_name="following", symmetrical=False
    )
    requested_to = models.ManyToManyField(
        "self", blank=True, related_name="requested_by", symmetrical=False
    )
    blocked_user = models.ManyToManyField(
        "self", blank=True, related_name="blocked_by", symmetrical=False
    )

    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
     related_query_name='hit_count_generic_relation')

    def __str__(self):
        return self.username


def photo_path_post(instance, filename):
    current_dateTime = datetime.now()
    basefilename, file_extension = os.path.splitext(filename)
    # chars= 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    # randomstr= ''.join((random.choice(chars)) for x in range(10))
    return 'posts/{basename}{username}-{randomstring}{ext}'.format(username=instance.user.username, basename="post-", randomstring=current_dateTime, ext=file_extension)


class Posts(models.Model):
    current_dateTime = datetime.now()
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_image = ProcessedImageField(upload_to=photo_path_post, help_text="Post",
                                     verbose_name="Post",
                                     processors=[ResizeToFill(400, 400)],
                                     format='JPEG',
                                     options={'quality': 80})
    caption = models.CharField(max_length=100, blank=True)
    uploaded_on = models.DateTimeField(default=timezone.now())
    in_repository=models.BooleanField(default=False)
    comments_disabled=models.BooleanField(default=False)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True,
        related_name="like"
    )

    def __str__(self):
        return (self.caption + "-" + self.user.username)

    def get_absolute_url(self):
        return reverse('home')
    @property
    def is_past_due(self):
        return date.today() > datetime.date(self.uploaded_on)

# Comment model links a comment with the post and the user.
class Comments(models.Model):
    post = models.ForeignKey(
        Posts, related_name='details', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='details', on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    comment_date = models.DateTimeField(default=timezone.now)
    @property
    def is_past_due(self):
        return  date.today() > datetime.date(self.comment_date)

# It stores the like info. It has the user who created the like and the post on which like was made.
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='loves', on_delete=models.CASCADE)
    post = models.ForeignKey(
        Posts, related_name='loves', on_delete=models.CASCADE)

    def __str__(self):
        return (self.user.username + " Liked " + self.post.caption + "(" + self.post.user.username + ")")

class IsSaved(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='savedpost', on_delete=models.CASCADE)
    post = models.ForeignKey(
        Posts, related_name='savedpost', on_delete=models.CASCADE)

    def __str__(self):
        return (self.user.username + " savedpost " + self.post.caption + "(" + self.post.user.username + ")")

def photo_path_story(instance, filename):
    current_dateTime = datetime.now()
    basefilename, file_extension = os.path.splitext(filename)
    # chars= 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    # randomstr= ''.join((random.choice(chars)) for x in range(10))
    return 'stories/{basename}{username}-{randomstring}{ext}'.format(username=instance.user.username, basename="story-", randomstring=current_dateTime, ext=file_extension)

class Tales(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='tales', on_delete=models.CASCADE)
    file = models.FileField(upload_to=photo_path_story)
    uploaded_on = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return (self.user.username + "-" + str(datetime.date(self.uploaded_on)))