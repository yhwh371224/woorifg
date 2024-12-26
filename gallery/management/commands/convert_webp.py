import os
from PIL import Image
from django.core.management.base import BaseCommand
from gallery.models import Gallery


class Command(BaseCommand):
    help = 'Convert existing JPG/PNG images to WebP format'

    def handle(self, *args, **kwargs):
        images_converted = 0
        gallery_dir = os.path.join('media', 'gallery') 

        if not os.path.exists(gallery_dir):
            os.makedirs(gallery_dir)

        for gallery in Gallery.objects.all():
            if gallery.head_image:
                img_path = gallery.head_image.path

                if not img_path.lower().endswith('.webp') and os.path.exists(img_path):
                    try:
                        img = Image.open(img_path)

                        if img.format not in ['WEBP']:
                            webp_path = os.path.join(gallery_dir, os.path.basename(img_path)) + '.webp'

                            if not os.path.exists(webp_path):
                                img.save(webp_path, 'WEBP', quality=80)

                                gallery.head_image.name = os.path.relpath(webp_path, 'media')
                                
                                os.remove(img_path)

                                gallery.save()

                                images_converted += 1
                                self.stdout.write(self.style.SUCCESS(f'Converted {img_path} to {webp_path}'))
                            else:
                                self.stdout.write(self.style.WARNING(f'{webp_path} already exists, skipping.'))

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error processing image {img_path}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Total images converted: {images_converted}'))
