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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator


class GalleryList(ListView):
    model = Gallery
    paginate_by = 12
    template_name = 'gallery/gallery_list.html'

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        queryset = Gallery.objects.all().order_by('-created')

        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=self.category)
        else:
            self.category = None

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        
        queryset = self.get_queryset()
       
        context['gallery_count'] = queryset.count()
        context['category_list'] = Category.objects.all()
        context['galleries_without_category'] = Gallery.objects.filter(category=None).count()
        context['category'] = self.category
        context['search_error'] = self.request.session.get('search_error', None)

        # 페이지네이션 처리
        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page', 1)

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
            category = get_object_or_404(Category, slug=slug)

        return Gallery.objects.filter(category=category).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['gallerys_without_category'] = Gallery.objects.filter(category=None).count()

        slug = self.kwargs['slug']

        if slug == '_none':
            context['category'] = '미분류'
        else:
            category = get_object_or_404(Category, slug=slug)
            context['category'] = category

        return context


@method_decorator(login_required, name='dispatch')
class ConvertWebpView(View):
    def post(self, request, *args, **kwargs):
        try:
            call_command('convert_webp')
            return JsonResponse({'status': 'success', 'message': 'Command executed successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
