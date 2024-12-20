import os
import PyPDF2

from django.http import JsonResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.conf import settings
from django.http import Http404
from django.core.exceptions import FieldError
from django.db.models import Q


from .models import Members, Bulletin, Pdf, Music, Category
from .forms import BulletinForm, PdfForm, MusicForm


def merge_latest_pdfs(request):
        # 최신 두 개의 Bulletin 객체를 가져옵니다.
        bulletins = Bulletin.objects.all().order_by('-created')[:2]

        if len(bulletins) < 2:
            return JsonResponse("주보가 두 개 이상 등록되어야 합니다.", status=400)

        merger = PyPDF2.PdfMerger()

        for bulletin in bulletins:
            if bulletin.pdf_file:
                file_path = bulletin.pdf_file.path
                print(f"파일 경로: {file_path}")  
                merger.append(file_path)

        merged_filename = f"{bulletins[0].date}_merged.pdf"
        merged_file_path = os.path.join(settings.MEDIA_ROOT, 'bulletins', merged_filename)

        try:
            with open(merged_file_path, 'wb') as merged_file:
                merger.write(merged_file)
        except Exception:
            return JsonResponse({"error": "병합된 PDF 저장 중 문제가 발생했습니다."}, status=500)
        finally:
            merger.close()


        merged_bulletin = Bulletin.objects.create(
            date=bulletins[0].date,  
            pdf_file=f'bulletins/{merged_filename}' 
        )
        
        # 병합 후 파일 삭제 및 객체 삭제
        for bulletin in bulletins:
            if bulletin.pdf_file:
                try:
                    # 파일이 열린 상태라면 닫기
                    if hasattr(bulletin.pdf_file, 'close'):
                        bulletin.pdf_file.close()

                    # 파일 삭제
                    os.remove(bulletin.pdf_file.path)
                except Exception as e:
                    return JsonResponse({"error": f"파일 삭제 실패: {str(e)}"}, status=500)

            # Bulletin 객체 삭제
            bulletin.delete()

        updated_bulletins = Bulletin.objects.all().order_by('-created')  

        bulletin_data = [
            {
                'date': bulletin.date,
                'pdf_file': bulletin.pdf_file.url
            } for bulletin in updated_bulletins
        ]

        return JsonResponse({"message": "주보 병합이 완료되었습니다.", "bulletins": bulletin_data})


class MemberListView(ListView):
    model = Members
    template_name = 'members_list.html'
    context_object_name = 'members'


class MemberDetailView(DetailView):
    model = Members
    template_name = 'member_detail.html'
    context_object_name = 'member'


class BulletinListView(ListView):
    model = Bulletin
    template_name = 'blog/bulletin_list.html'
    context_object_name = 'bulletins'
    queryset = Bulletin.objects.all().order_by('-created')
    paginate_by = 4 
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BulletinForm()  # 폼을 컨텍스트에 추가
        return context

    def post(self, request, *args, **kwargs):
        form = BulletinForm(request.POST, request.FILES)  
        
        if form.is_valid():
            form.save()
            return redirect('bulletin_list')  

        return self.render_to_response(self.get_context_data(form=form))
    

class BulletinDetailView(DetailView):
    model = Bulletin
    template_name = 'bulletins/bulletin_detail.html'
    context_object_name = 'bulletin'


class BulletinUploadView(LoginRequiredMixin, CreateView):
    model = Bulletin
    form_class = BulletinForm
    template_name = 'blog/bulletin_upload.html'
    success_url = reverse_lazy('bulletin_list') 

    def form_valid(self, form):        
        return super().form_valid(form)
    
    def get_login_url(self):
        login_url = super().get_login_url() or reverse_lazy('account_login')
        return f'{login_url}?next={self.request.path}'  


# pdf views.py
class PdfListView(ListView):
    model = Pdf
    template_name = 'blog/pdf_list.html'
    context_object_name = 'pdfs'
    queryset = Pdf.objects.all().order_by('-created')
    paginate_by = 4 
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PdfForm()  # 폼을 컨텍스트에 추가
        return context

    def post(self, request, *args, **kwargs):
        form = PdfForm(request.POST, request.FILES)  
        
        if form.is_valid():
            form.save()
            return redirect('pdf_list')  

        return self.render_to_response(self.get_context_data(form=form))
    

class PdfDetailView(DetailView):
    model = Pdf
    template_name = 'pdfs/pdf_detail.html'
    context_object_name = 'pdf'


class PdfUploadView(LoginRequiredMixin, CreateView):
    model = Pdf
    form_class = PdfForm
    template_name = 'blog/pdf_upload.html'
    success_url = reverse_lazy('pdf_list') 

    def form_valid(self, form):        
        return super().form_valid(form)
    
    def get_login_url(self):
        login_url = super().get_login_url() or reverse_lazy('account_login')
        return f'{login_url}?next={self.request.path}'
    

class PdfSearch(PdfListView):
    def get_queryset(self):
        q = self.kwargs['q']
        try:
            object_list = Music.objects.filter(
                Q(title__icontains=q) | 
                Q(date__icontains=q)   
            )
        except FieldError:
            raise Http404(f"No results found for '{q}'")
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_info'] = f'Search: "{self.kwargs["q"]}"'
        return context


class MusicListView(ListView):
    model = Music
    template_name = 'blog/music_list.html'
    context_object_name = 'musics'
    queryset = Music.objects.all().order_by('-created')
    paginate_by = 4 
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PdfForm()  # 폼을 컨텍스트에 추가
        return context

    def post(self, request, *args, **kwargs):
        form = MusicForm(request.POST, request.FILES)  
        
        if form.is_valid():
            form.save()
            return redirect('pdf_list')  

        return self.render_to_response(self.get_context_data(form=form))
    

class MusicDetailView(DetailView):
    model = Music
    template_name = 'musics/music_detail.html'
    context_object_name = 'music'


class MusicUploadView(LoginRequiredMixin, CreateView):
    model = Music
    form_class = MusicForm
    template_name = 'blog/music_upload.html'
    success_url = reverse_lazy('music_list') 

    def form_valid(self, form):        
        return super().form_valid(form)
    
    def get_login_url(self):
        login_url = super().get_login_url() or reverse_lazy('account_login')
        return f'{login_url}?next={self.request.path}'
    

class MusicSearch(MusicListView):
    def get_queryset(self):
        q = self.kwargs['q']
        try:
            object_list = Music.objects.filter(
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


class MusicListByCategory(ListView):

    def get_queryset(self):
        slug = self.kwargs['slug']

        if slug == '_none':
            category = None
        else:
            category = Category.objects.get(slug=slug)

        return Music.objects.filter(category=category).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['musics_without_category'] = Music.objects.filter(category=None).count()

        slug = self.kwargs['slug']

        if slug == '_none':
            context['category'] = '미분류'
        else:
            category = Category.objects.get(slug=slug)
            context['category'] = category

        return context