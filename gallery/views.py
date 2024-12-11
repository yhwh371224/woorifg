from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Gallery
from .forms import GalleryForm


class GalleryList(ListView):
    model = Gallery
    template_name = 'gallery/gallery_list.html'
    paginate_by = 7

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery_count'] = Gallery.objects.all().count()
        context['user_name'] = self.request.user.username
        context['search_error'] = self.request.session.get('search_error', None)
        return context


class GalleryCreate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = GalleryForm(initial={'name': request.user.username})
        return render(request, 'gallery/gallery_form.html', {'form': form, 'form_guide': 'Please upload your gallery'})

    def post(self, request, *args, **kwargs):
        form = GalleryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/gallery/')
        return render(request, 'gallery/gallery_form.html', {'form': form, 'form_guide': 'Please upload your gallery'})


class GalleryDetail(DetailView):
    model = Gallery
    template_name = 'gallery/gallery_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery_count'] = Gallery.objects.all().count()
        user_name = self.request.user.username
        context['user_name'] = user_name
        return context


class GalleryUpdate(LoginRequiredMixin, UpdateView):
    model = Gallery
    template_name = 'gallery/gallery_form.html'
    fields = ['date', 'title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_name = self.request.user.username
        context['user_name'] = user_name
        return context


def index(request):
    Gallerys = Gallery.objects.all()
    return render(request, 'gallery/index.html', {'Gallerys': Gallerys})
