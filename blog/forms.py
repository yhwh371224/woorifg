from django import forms
from .models import Bulletin, Pdf


class BulletinForm(forms.ModelForm):
    class Meta:
        model = Bulletin
        fields = ['date', 'pdf_file']


class PdfForm(forms.ModelForm):
    class Meta:
        model = Pdf
        fields = ['title', 'date', 'pdf_file']
