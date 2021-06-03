from django.db import models
#from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from tinymce.models import HTMLField
from django.conf import settings

User = settings.AUTH_USER_MODEL

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(default=18)
    date_joined = models.DateTimeField(auto_now_add=True)
    # add additional fields in here

    def __str__(self):
        return self.username


# Create your models here.

"""class PostViews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip = models.CharField(max_length=15, null=True, blank=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username"""

class Comment(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(max_length=5000)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True
    )
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return 'Anonymous'

class Author(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name =  models.CharField(max_length=20, null=True)
    profile_picture = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def profile_picURL(self):
        try:
            url = self.profile_picture.url
        except:
            url = ''
        return url


class Category(models.Model):
    title = models.CharField(max_length= 20)

    def __str__(self):
        return self.title

from analytics.models import ObjectViewed

class Post(models.Model):
    title = models.CharField(max_length=100)
    keywords = models.CharField(max_length=100, null=True, blank=True)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField(default="test")
    #comment_count = models.IntegerField(default = 0)
    #view_count = models.IntegerField(default = 0)
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    thumbnail = models.ImageField(upload_to='images/', null=True, blank=True)
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField(default = False)
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)
        
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_view', kwargs={
            'pk': self.pk,
            })

    def get_update_url(self):
        return reverse('post_update_view', kwargs={
            'pk': self.pk,
            })

    def get_view_count(self):
        view_count = ObjectViewed.objects.filter(object_id=self.id).values('ip_address')
        unique_ip_views = set()
        for view in view_count:
            for value in view.values():
                unique_ip_views.add(str(value))
        unique_views_number = 0
        for u_view in unique_ip_views:
            unique_views_number += 1
        return unique_views_number

    """def get_delete_url(self):
        return reverse('post_delete_view', kwargs={
            'pk': self.pk,
            })"""

    @property
    def thumbnailURL(self):
        try:
            url = self.thumbnail.url
        except:
            url = ''
        return url

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

    """@property
    def view_count(self):
        return PostViews.objects.filter(post=self).count()"""
    

class ContactModel(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=5000)

    def __str__(self):
        return self.subject
