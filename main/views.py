from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

from analytics.mixins import ObjectViewMixin, FilterViewMixin, SearchViewMixin
from .models import *
from analytics.models import ObjectViewed
from .forms import *
# Create your views here.

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def get_categories():
    categories = Category.objects.all().values()
    categories_count = Post.objects.values('categories__title').annotate(Count('categories'))
    full_list = []

    for item in categories:
        for unit in categories_count:
            if item['title'] == unit['categories__title']:
                what_i_need = {}       
                what_i_need['id'] = item['id']
                what_i_need['title'] = item['title']
                what_i_need['category_count'] = unit['categories__count']
                full_list.append(what_i_need)

    return full_list


class searchView(SearchViewMixin, ListView):
    template_name='blog.html'
    context_object_name='queryset'
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.all()
        query = self.request.GET.get('q')
        return queryset.filter(Q(title__icontains=query) |Q(overview__icontains=query)).distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        categories = get_categories()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context['most_recent'] = most_recent
        context['testing'] = categories
        context["q"] = f'q={self.request.GET.get("q")}&'
        context['page_request_var'] = 'page'
        return context





class indexView(View):
    def get(self, request, *args, **kwargs):
        featured = Post.objects.filter(featured=True)
        latest = Post.objects.order_by('-timestamp')[0:3]
        context = {
            'object_list': featured,
            'latest': latest,
        }
        return render(request, 'index.html', context)


class blogView(ListView):
    model = Post
    template_name='blog.html'
    #default context_object_name = object_list
    context_object_name='queryset'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        categories = get_categories()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['page_request_var'] = 'page'
        context['most_recent'] = most_recent
        context['testing'] = categories
        return context





class postView(ObjectViewMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form = CommentForm()

    def get_object(self):
        obj = super().get_object()
        #object_viewed_signal.send(obj.__class__, intance=obj, request=self.request)
        """if self.request.user.is_authenticated:
            PostViews.objects.get_or_create(
                user=self.request.user,
                post=obj
            )"""
        return obj

    def get_context_data(self, **kwargs):
        categories = get_categories()
        #current_post = super().get_object()
        most_recent = Post.objects.order_by('-timestamp')[:3]

        context = super().get_context_data(**kwargs)
        context['page_request_var'] = 'page'
        context['most_recent'] = most_recent
        context['testing'] = categories
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
           # print(form)
            print("Valid Form")
            post = self.get_object()
            if request.user.id == None:
                email = form.cleaned_data['email']
                name = form.cleaned_data['name']
            else:
                user = request.user
                email = user.email
                name = user.first_name + user.last_name
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse ('post_view', kwargs = {'pk': post.pk }))
        else :
            """print(form)
            print("Invalid Form")
            print(form.errors)"""
            post = self.get_object()
            return redirect(reverse ('post_view', kwargs = {'pk': post.pk }))



class postCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect('post_view', form.instance.pk)



class postUpdateView(UpdateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect('post_view', form.instance.pk)



class postDeleteView(DeleteView):
    model = Post
    success_url = '/blog'
    template_name = 'post_delete.html'





class FilterView(FilterViewMixin, ListView):
    template_name='blog.html'
    context_object_name='queryset'
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.filter(categories__in=self.request.GET.getlist("category")).distinct()
        #object_viewed_signal.send(queryset=queryset, request=self.request)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        categories = get_categories()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context['most_recent'] = most_recent
        context["category"] = ''.join([f"category={x}&" for x in self.request.GET.getlist("category")])
        context['testing'] = categories
        context['page_request_var'] = 'page'
        return context




def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
        #print(form)
    else:
        form = ContactForm(request.POST)
        #print(form)
        print("Invalid Form")
        print(form.errors)
        if form.is_valid():
            #print(form)
            print("Valid Form")
            subject = form.cleaned_data['subject']
            if request.user.id == None:
                email = form.cleaned_data['email']
            else:
                user = request.user
                email = user.email
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, email, ['menhior1@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')

    return render(request, "email/contact.html", {'form': form})

def successView(request):
    return render(request, "email/success.html", {})


class testView(ObjectViewMixin, DetailView):
    model = Post
    template_name = 'test.html'
    context_object_name = 'post'
    form = TestCommentForm()

    def get_object(self):
        obj = super().get_object()
        #object_viewed_signal.send(obj.__class__, intance=obj, request=self.request)
        """if self.request.user.is_authenticated:
            PostViews.objects.get_or_create(
                user=self.request.user,
                post=obj
            )"""
        return obj

    def get_context_data(self, **kwargs):
        categories = get_categories()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['page_request_var'] = 'page'
        context['most_recent'] = most_recent
        context['testing'] = categories
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            #print(form)
            print("Valid Form")
            post = self.get_object()
            if request.user.id == None:
                email = form.cleaned_data['email']
                name = form.cleaned_data['name']
            else:
                user = request.user
                email = user.email
                name = user.first_name + user.last_name            
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse ('test', kwargs = {'pk': post.pk }))
        else :
            """print(form)
            print("Invalid Form")
            print(form.errors)"""
            post = self.get_object()
            return redirect(reverse ('test', kwargs = {'pk': post.pk }))