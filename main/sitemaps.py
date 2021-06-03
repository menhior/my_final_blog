from django.contrib.sitemaps import  Sitemap
from .models import Post
from django.shortcuts import reverse


class StaticViewSitemap(Sitemap):
	def items(self):
		return ['index_view', 'blog_view', 'contact' ]

	def location(self, item):
		return reverse(item)


class PostSitemap(Sitemap):
    def items(self):
        return  Post.objects.all()