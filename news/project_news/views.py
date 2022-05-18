from .models import Author, Category, Comment, Post, PostCategory, User
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .filters import PostFilter
from .forms import PostForm
from .models import *
from django.shortcuts import *
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class AddProtectedView(PermissionRequiredMixin, CreateView):
#    template_name = '../../news/templates/add_article.html'
    form_class = PostForm
    template_name = 'add_article.html'
#    login_url='/accounts/login'
    permission_required = ('posts.add_post')
    model = Post
    queryset = Post.objects.all()

    def form_valid(self, form):
        self.object = form.save(commit= False)
        author = self.request.user
        id = Author.objects.get(author= User.objects.get(username = author)).id
        self.object.author_id = id
        self.object.save()
        return  super().form_valid(form)

class AuthorsList(ListView):
    model = Author
    template_name = 'authors.html'
    context_object_name = 'authors'
    queryset = Author.objects.order_by('-id')

class AuthorDetail(DetailView):
    model = Author
    template_name = 'author.html'
    context_object_name = 'author'

class FilteredListView(ListView):
    filterset_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_count'] = len(Post.objects.all())
        return context

    def post_1(self, request, *args, **kwargs):
        form = self.form_class(request.POST_1)

        if form.is_valid():  
            form.save()
        return super().get(request, *args, **kwargs)


class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 3

    def get_queryset(self):
        queryset=super().get_queryset()
        self.filterset=PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    context_object_name = 'post_create'

class PostUpdate(PermissionRequiredMixin, UpdateView):
#    template_name = '../../news/templates/add_article.html'
    form_class = PostForm
    template_name = 'add_article.html'
    context_object_name = 'post_update'
    permission_required = ('posts.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url=reverse_lazy('post_list')

