import os
from PIL import Image
from django.core.management.base import BaseCommand
from django.conf import settings
from gallery.models import Gallery


class Command(BaseCommand):
    help = 'Convert the most recent image to WebP format, resize it, and rotate it -90 degrees'

    MAX_WIDTH = 2000
    MAX_HEIGHT = 2000

    def handle(self, *args, **kwargs):
        gallery = Gallery.objects.order_by('-id').first()
        if not gallery or not os.path.exists(gallery.head_image.path):
            return

        img_path = gallery.head_image.path
        img_dir, img_filename = os.path.split(img_path)
        img_name, img_ext = os.path.splitext(img_filename)
        webp_path = os.path.join(img_dir, f"{img_name}.webp")

        with Image.open(img_path) as img:
            if img_ext.lower() in ['.jpg', '.jpeg']:
                img = img.rotate(-90, expand=True)
            img.thumbnail((self.MAX_WIDTH, self.MAX_HEIGHT), Image.Resampling.BILINEAR)
            img.save(webp_path, 'WEBP')

        gallery.head_image.name = os.path.relpath(webp_path, settings.MEDIA_ROOT)
        gallery.save(update_fields=['head_image'])
        os.remove(img_path)

