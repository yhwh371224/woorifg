from django.db import models
from django.contrib.auth.models import User


class Members(models.Model):
    english_name = models.CharField(max_length=50, blank=False)
    korean_name = models.CharField(max_length=50, blank=False)
    contact = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=False, db_index=True, verbose_name='email') 
    street = models.CharField(max_length=50, blank=True)   
    suburb = models.CharField(max_length=50, blank=True)
    birthday = models.DateField(blank=True, null=True)
    children = models.CharField(max_length=50, blank=True)
    position = models.CharField(max_length=50, blank=True)
    vehicle = models.BooleanField(default=False, blank=True)
    attendence = models.BooleanField(default=False, blank=True)
    message = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created'] 

    def __str__(self):
        return f"{self.korean_name} ({self.english_name})"
    

class Bulletin(models.Model): 
    date = models.DateField(blank=True, null=True, verbose_name='ex)2024-12-31 ')  
    pdf_file = models.FileField(upload_to='bulletins/', null=True, blank=True, verbose_name='주보 PDF 파일 ')    
    created = models.DateTimeField(auto_now_add=True)  

    class Meta:
        verbose_name = 'Bulletin'
        verbose_name_plural = 'Bulletins'
        ordering = ['-created']  

    def __str__(self):
        return f"{self.date}"
 

class Pdf(models.Model): 
    title = models.CharField(max_length=100, blank=False, null=True)
    date = models.DateField(blank=True, null=True, verbose_name='ex)2024-12-31 ')  
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True, verbose_name='PDF 파일 ')    
    created = models.DateTimeField(auto_now_add=True)  

    class Meta:
        verbose_name = 'Pdf'
        verbose_name_plural = 'Pdfs'
        ordering = ['-created']  

    def __str__(self):
        return f"{self.date}"
    

class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/music/category/{}/'.format(self.slug)

    class Meta:
        verbose_name_plural = 'categories'
    

class Music(models.Model): 
    title = models.CharField(max_length=100, blank=False, null=True)
    date = models.DateField(blank=True, null=True, verbose_name='ex)2024-12-31 ')  
    pdf_file = models.FileField(upload_to='musics/', null=True, blank=True, verbose_name='찬양 PDF 파일 ') 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)   
    created = models.DateTimeField(auto_now_add=True)  

    class Meta:
        verbose_name = 'Music'
        verbose_name_plural = 'Musics'
        ordering = ['-created']  

    def __str__(self):
        return f"{self.date}"




