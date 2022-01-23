from django.contrib.sitemaps import  Sitemap
from .models import Post
from django.shortcuts import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.8
    protocol = 'https'

    
    def items(self):
        return ['index_view', 'blog_view', 'contact' ]

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return  Post.objects.all()

    def lastmod(self, obj):
        return obj.timestamp

    def location(self,obj):
        return '/blog/%s' % (obj.slug)