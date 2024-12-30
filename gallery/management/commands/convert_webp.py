import os
from PIL import Image, ImageOps, UnidentifiedImageError
from django.core.management.base import BaseCommand
from django.conf import settings
from gallery.models import Gallery


class Command(BaseCommand):
    help = 'Convert the most recent image to WebP format, resize it, and rotate it -90 degrees'

    # 최대 이미지 크기 (너비, 높이)
    MAX_WIDTH = 2000
    MAX_HEIGHT = 2000

    def handle(self, *args, **kwargs):
        images_converted = 0

        self.stdout.write(self.style.SUCCESS('Processing the most recent image...'))

        # 가장 최근 객체 하나 가져오기
        gallery = Gallery.objects.order_by('-id').first()

        if not gallery or not gallery.head_image or not gallery.head_image.name:
            self.stdout.write(self.style.WARNING('No suitable image found to process.'))
            return

        img_path = gallery.head_image.path

        if not os.path.exists(img_path):
            self.stdout.write(self.style.WARNING(f'File does not exist: {img_path}'))
            return

        try:
            with Image.open(img_path) as img:
                img_dir, img_filename = os.path.split(img_path)
                img_name, img_ext = os.path.splitext(img_filename)

                # Apply Exif orientation if exists
                if img.getexif():
                    img = ImageOps.exif_transpose(img)
                else:
                    img = img.rotate(-90, expand=True)

                # Resize if image exceeds max dimensions
                img.thumbnail((self.MAX_WIDTH, self.MAX_HEIGHT), Image.Resampling.NEAREST)

                # Save as WebP
                webp_path = os.path.join(img_dir, f"{img_name}.webp")
                img.save(webp_path, 'WEBP')

                if os.path.exists(webp_path):
                    # Update database record
                    gallery.head_image.name = os.path.relpath(webp_path, settings.MEDIA_ROOT)
                    gallery.save(update_fields=['head_image'])

                    # Remove original image
                    os.remove(img_path)
                    images_converted += 1

                    self.stdout.write(self.style.SUCCESS(f'Converted, resized, and rotated {img_path} to {webp_path}'))
                else:
                    self.stdout.write(self.style.ERROR(f'Failed to save WebP image: {webp_path}'))

        except UnidentifiedImageError:
            self.stdout.write(self.style.ERROR(f'Cannot identify image file: {img_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing image {img_path}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Total images converted: {images_converted}'))
