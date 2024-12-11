import datetime
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post, Comment
from .forms import CommentForm, PostForm


class PostList(ListView):
    model = Post
    template_name = 'review/post_list.html'
    paginate_by = 7

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['post_count'] = Post.objects.all().count()

        user_name = None
        if self.request.user.is_authenticated:
            user_name = self.request.user.username  

        context['user_name'] = user_name
        context['search_error'] = self.request.session.get('search_error', None)

        return context
    

class PostDetail(DetailView):
    model = Post
    template_name = 'review/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_count'] = Post.objects.all().count()
        context['comment_form'] = CommentForm()

        user_name = None
        if self.request.user.is_authenticated:
            user_name = self.request.user.username  

        context['user_name'] = user_name

        return context
    

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'review/post_form.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_name'] = self.request.user.username
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user.username  
        post.name = self.request.user.username
        if not post.date:
            post.date = datetime.date.today()
        post.save()
        return redirect('review:post_detail', pk=post.pk)


class PostUpdate(UpdateView):
    model = Post
    template_name = 'review/post_form.html'
    fields = ['content', 'title', 'date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_name'] = self.request.user.username
        return context


class CommentCreate(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        user_name = None
        if request.user.is_authenticated:
            user_name = request.user.username  

        comment_form = CommentForm()
        
        context = {
            'post': post,
            'user_name': user_name,
            'comment_form': comment_form,
        }

        return render(request, 'review/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        user_name = None
        if request.user.is_authenticated:
            user_name = request.user.username  

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = user_name
            comment.save()
            return redirect(post.get_absolute_url())  

        context = {
            'post': post,
            'user_name': user_name,
            'comment_form': comment_form,
        }
        return render(request, 'review/post_detail.html', context)


class CommentUpdate(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'review/comment_form.html'

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)        
        user_name = None

        if self.request.user.is_authenticated:
            user_name = self.request.user.username  

        if comment.author != user_name:
            raise PermissionDenied('No right to edit')

        return comment
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_name = None
        if self.request.user.is_authenticated:
            user_name = self.request.user.username  

        context['user_name'] = user_name
        return context

    def get_success_url(self):
        post = self.get_object().post
        return post.get_absolute_url() + '#comment-list'


class CommentDelete(DeleteView):
    model = Comment
    template_name = 'review/comment_confirm_delete.html'

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)        
        user_name = None

        if self.request.user.is_authenticated:
            user_name = self.request.user.username  

        if comment.author != user_name:
            raise PermissionDenied('No right to delete Comment')

        return comment
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_name = None
        if self.request.user.is_authenticated:
            user_name = self.request.user.username  

        context['user_name'] = user_name
        return context

    def get_success_url(self):
        post = self.get_object().post
        return post.get_absolute_url() + '#comment-list'
