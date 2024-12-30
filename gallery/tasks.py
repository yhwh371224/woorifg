from celery import shared_task
from django.conf import settings
from .models import Gallery
from PIL import Image
import os

MAX_WIDTH = 2000
MAX_HEIGHT = 2000

@shared_task
def process_gallery_image():
    gallery = Gallery.objects.order_by('-id').first()
    if not gallery or not os.path.exists(gallery.head_image.path):
        return

    img_path = gallery.head_image.path
    img_dir, img_filename = os.path.split(img_path)
    img_name, _ = os.path.splitext(img_filename)
    webp_path = os.path.join(img_dir, f"{img_name}.webp")

    with Image.open(img_path) as img:
        img = img.rotate(-90, expand=True)
        img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.Resampling.BILINEAR)
        img.save(webp_path, 'WEBP')

    gallery.head_image.name = os.path.relpath(webp_path, settings.MEDIA_ROOT)
    gallery.save(update_fields=['head_image'])
    os.remove(img_path)