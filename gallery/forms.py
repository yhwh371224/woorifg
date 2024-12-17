from .models import Gallery
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ('title', 'date', 'category', 'head_image')        
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['class'] = 'datepicker' 


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('text',)