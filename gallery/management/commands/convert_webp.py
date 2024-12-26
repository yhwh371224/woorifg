from django.core.management.base import BaseCommand
from gallery.models import Gallery
from PIL import Image
import os


class Command(BaseCommand):
    help = 'Convert existing JPG/PNG images to WebP format'

    def handle(self, *args, **kwargs):
        images_converted = 0

        for gallery in Gallery.objects.all():
            if gallery.head_image:
                img_path = gallery.head_image.path
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    if img.format != 'WEBP':
                        webp_path = os.path.splitext(img_path)[0] + '.webp'
                        img.save(webp_path, 'WEBP', quality=80)
                        gallery.head_image.name = os.path.relpath(webp_path, os.path.dirname(gallery.head_image.path))
                        os.remove(img_path)  # 원본 JPG/PNG 삭제
                        gallery.save()
                        images_converted += 1
                        self.stdout.write(self.style.SUCCESS(f'Converted {img_path} to {webp_path}'))

        self.stdout.write(self.style.SUCCESS(f'Total images converted: {images_converted}'))
