import os
import PyPDF2

from django.http import JsonResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.conf import settings

from .models import Members, Bulletin
from .forms import BulletinForm


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

        with open(merged_file_path, 'wb') as merged_file:
            merger.write(merged_file)

        merged_bulletin = Bulletin.objects.create(
            date=bulletins[0].date,  
            pdf_file=f'bulletins/{merged_filename}' 
        )

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
        return f'{super().get_login_url()}?next={self.request.path}'   

