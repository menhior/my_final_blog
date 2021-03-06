from django.db import models
from django.db.models.signals import pre_save, post_save
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
#from django.contrib.auth.models import User
from .signals import  object_viewed_signal, filter_signal, search_signal
from main.models import Category
from ipware import get_client_ip

from django.conf import settings

User = settings.AUTH_USER_MODEL

class ObjectViewed(models.Model):
    user            = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    content_type    = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id       = models.PositiveIntegerField()
    ip_address      = models.CharField(max_length=120, blank=True, null=True)
    content_object  = GenericForeignKey('content_type', 'object_id')
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self, ):
        return "%s viewed: %s" %(self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object Viewed'
        verbose_name_plural = 'Objects Viewed'

def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    try:
        ip_address, is_routable = get_client_ip(request)
    except:
        pass
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    new_view_instance = ObjectViewed.objects.create(
                user=user, 
                content_type=c_type,
                object_id=instance.id,
                ip_address=ip_address
                )

object_viewed_signal.connect(object_viewed_receiver)




class UserSearch(models.Model):
    user            = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    ip_address      = models.CharField(max_length=120, blank=True, null=True)
    search          = models.CharField(max_length=100, blank=True, null=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return "%s searched: %s at %s" %(self.user, self.search, self.timestamp) 
        else:
            return "%s searched: %s at %s" %(self.ip_address, self.search, self.timestamp)


def search_receiver(sender, queryset, request, *args, **kwargs):
    try:
        ip_address, is_routable = get_client_ip(request)
    except:
        pass

    if request.user.is_authenticated:
        user = request.user
    else:
        user = None


    UserSearch.objects.create(
            user=user,
            ip_address=ip_address,
            search=request.GET.get("q"),
        )

search_signal.connect(search_receiver)

class UserFilter(models.Model):
    user            = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    ip_address      = models.CharField(max_length=120, blank=True, null=True)
    categories      = models.CharField(max_length=100, blank=True, null=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return "%s filtered: %s at %s" %(self.user, self.categories, self.timestamp) 
        else:
            return "%s filtered: %s at %s" %(self.ip_address, self.categories, self.timestamp)


def filter_receiver(sender, queryset, request, *args, **kwargs):
    try:
        ip_address, is_routable = get_client_ip(request)
    except:
        pass

    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    list_of_categories = []
    category_string = ''

    for i in request.GET.getlist("category"):
        list_of_categories.append(Category.objects.get(id=i))
        #Category.objects.get(id=i)
    for i in list_of_categories:
        category_string += str(i) + ', '
    print(category_string)

    UserFilter.objects.create(
            user=user,
            ip_address=ip_address,
            categories=category_string,
        )

filter_signal.connect(filter_receiver)