from .models import Gallery
from django import forms


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ('title', 'date', 'author', 'head_image')        
    
    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['class'] = 'datepicker' 

        # 'author' 필드를 초기값으로 로그인한 사용자의 username을 설정
        # if 'author' not in self.initial:
        #     self.initial['author'] = kwargs.get('initial', {}).get('author', None)
