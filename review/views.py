import datetime
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.db.models import Q
from django.views import View
from django.http import Http404
from django.core.exceptions import FieldError
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, Category
from .forms import CommentForm, PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404


class PostList(ListView):
    model = Post
    template_name = 'review/post_list.html'
    paginate_by = 4

    def get_queryset(self):
        category_slug = self.request.GET.get('category_slug')
        queryset = Post.objects.all().order_by('-created')

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
            self.category = category  
        else:
            self.category = None  
        
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        queryset = self.get_queryset()

        context['post_count'] = queryset.count()
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()
        context['search_error'] = self.request.session.get('search_error', None)
        context['category'] = self.category  
       
        page = self.request.GET.get('page', 1)
        paginator = Paginator(queryset, self.paginate_by)

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context['page_obj'] = page_obj
        context['paginator'] = paginator
        context['total_pages'] = paginator.num_pages

        return context
    

class PostDetail(DetailView):
    model = Post
    template_name = 'review/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_count'] = Post.objects.all().count()
        context['comment_form'] = CommentForm()

        return context
    

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'review/post_form.html'
    form_class = PostForm
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user.username  
        post.name = self.request.user.username
        if not post.date:
            post.date = datetime.date.today()
        post.save()
        return redirect('review:review_detail', pk=post.pk)

    def get_login_url(self):
        login_url = super().get_login_url() or reverse_lazy('account_login')
        return f'{login_url}?next={self.request.path}'
    

class PostUpdate(UpdateView):
    model = Post
    template_name = 'review/post_form.html'
    fields = ['content', 'title', 'date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class CommentCreate(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        comment_form = CommentForm()
        
        context = {
            'post': post,
            'comment_form': comment_form,
        }

        return render(request, 'review/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = self.request.user
            comment.save()
            return redirect(post.get_absolute_url())  

        context = {
            'post': post,
            'comment_form': comment_form,
        }
        return render(request, 'review/post_detail.html', context)


class CommentUpdate(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'review/comment_form.html'

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)        

        if comment.author != self.request.user:
            raise PermissionDenied('No right to edit')

        return comment
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        post = self.get_object().post
        return post.get_absolute_url() + '#comment-list'


class CommentDelete(DeleteView):
    model = Comment
    template_name = 'review/comment_confirm_delete.html'

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)        

        if comment.author != self.request.user:
            raise PermissionDenied('No right to edit')


        return comment
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        post = self.get_object().post
        return post.get_absolute_url() + '#comment-list'
    

class PostSearch(PostList):
    def get_queryset(self):
        q = self.kwargs['q']
        try:
            object_list = Post.objects.filter(
                Q(title__icontains=q) | 
                Q(content__icontains=q) | 
                Q(name__icontains=q)  
            )
        except FieldError:
            raise Http404(f"No results found for '{q}'")
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_info'] = f'Search: "{self.kwargs["q"]}"'
        context['category'] = self.kwargs.get('category', 'Search Results')
        return context
    

class PostCategory(ListView):

    def get_queryset(self):
        slug = self.kwargs['slug']

        if slug == '_none':
            category = None
        else:
            category = Category.objects.get(slug=slug)

        return Post.objects.filter(category=category).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()

        slug = self.kwargs['slug']

        if slug == '_none':
            context['category'] = '미분류'
        else:
            category = Category.objects.get(slug=slug)
            context['category'] = category

        return context
