from django.urls import path

from django.contrib.auth import views as auth_views

from . import views



urlpatterns = [
	path('', views.indexView.as_view(), name = 'index_view'),
	path('blog/', views.blogView.as_view(), name = 'blog_view'),
	#path('post/<str:pk>/', views.postView.as_view(), name = 'post_view'),
	path('post/<slug:slug>/', views.postView.as_view(), name = 'post_view'),
	path('post_create/', views.postCreateView.as_view(), name = 'post_create_view'),
	#path('post/<str:pk>/update/', views.postUpdateView.as_view(), name = 'post_update_view'),
	path('post/<slug:slug>/update/', views.postUpdateView.as_view(), name = 'post_update_view'),
	#path('post/<str:pk>/delete/', views.postDeleteView.as_view(), name = 'post_delete_view'),
	path('post/<slug:slug>/delete/', views.postDeleteView.as_view(), name = 'post_delete_view'),
	path('search/', views.searchView.as_view(), name = 'search_view'),
	path("filter/", views.FilterView.as_view(), name='filter'),


	path('contact/', views.contactView, name='contact'),
    path('success/', views.successView, name='success'),

	path('test/<str:pk>/', views.testView.as_view(), name = 'test'),
]