import os
from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.conf import settings


def index(request): return redirect('/home/')


def home(request): return render(request, 'basecamp/home.html')


def introduction(request):     
    return render(request, 'basecamp/introduction.html')


def bulletin_list(request):     
    return render(request, 'basecamp/bulletin_list.html')


def meetings(request):     
    return render(request, 'basecamp/meetings.html')


def sitemap(request): 
    return render(request, 'basecamp/sitemap.xml')


def workers(request): 
    return render(request, 'basecamp/workers.html')


def column(request):
    return render(request, 'basecamp/column.html')


def location(request):
    return render(request, 'basecamp/location.html')


def worship_music(request):
    return render(request, 'basecamp/worship_music.html')


@login_required
def serve_pdf(request):
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'protected', 'contact_list.pdf')
    try:
        return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        return render(request, '404.html', status=404)
    

from django.shortcuts import render


# error handler 400 403 404 500 502 503 
def custom_bad_request(request, exception):
    return render(request, '400.html', status=400)


def custom_forbidden(request, exception):
    return render(request, '403.html', status=403)


def custom_page_not_found(request, exception):
    return render(request, '404.html', status=404)


def custom_server_error(request):
    return render(request, '500.html', status=500)


def custom_bad_gateway(request):
    return render(request, '502.html', status=502)


def custom_under_maintenance(request):
    return render(request, '503.html', status=503)






