from django.shortcuts import render, redirect
from .models import Gallery, Category
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import Http404
from django.core.exceptions import FieldError
from django.http import JsonResponse
from django.core.management import call_command
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST



class GalleryList(ListView):
    model = Gallery
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GalleryList, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Gallery.objects.filter(category=None).count()

        return context


class GallerySearch(GalleryList):
    def get_queryset(self):
        q = self.kwargs['q']
        try:
            object_list = Gallery.objects.filter(
                Q(title__icontains=q) | 
                Q(category__name__icontains=q)  
            )
        except FieldError:
            raise Http404(f"No results found for '{q}'")
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_info'] = f'Search: "{self.kwargs["q"]}"'
        return context


class GalleryDetail(DetailView):
    model = Gallery

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GalleryDetail, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['gallerys_without_category'] = Gallery.objects.filter(category=None).count()

        return context


class GalleryCreate(LoginRequiredMixin, CreateView):
    model = Gallery
    fields = [
        'title', 'date', 'head_image', 'category'
    ]

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super().form_valid(form)
        else:
            return redirect(self.get_login_url())
        
    def get_success_url(self):
        return reverse_lazy('gallery:gallery_detail', kwargs={'pk': self.object.pk})

    def get_login_url(self):
        login_url = super().get_login_url() or reverse_lazy('account_login')
        return f'{login_url}?next={self.request.path}'


class GalleryUpdate(UpdateView):
    model = Gallery
    fields = [
        'title', 'date', 'head_image', 'category'
    ]


class GalleryListByCategory(ListView):

    def get_queryset(self):
        slug = self.kwargs['slug']

        if slug == '_none':
            category = None
        else:
            category = Category.objects.get(slug=slug)

        return Gallery.objects.filter(category=category).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['gallerys_without_category'] = Gallery.objects.filter(category=None).count()

        slug = self.kwargs['slug']

        if slug == '_none':
            context['category'] = '미분류'
        else:
            category = Category.objects.get(slug=slug)
            context['category'] = category

        # context['title'] = 'Blog - {}'.format(category.name)
        return context


@login_required
@require_POST
def run_image_conversion(request):
    try:
        call_command('convert_webp')  # 커맨드 호출
        return JsonResponse({'status': 'success', 'message': 'Image converted successfully!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
