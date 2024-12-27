import os
from PIL import Image, ImageOps
from django.core.management.base import BaseCommand
from django.conf import settings
from gallery.models import Gallery


class Command(BaseCommand):
    help = 'Convert existing JPG/PNG images to WebP format and rotate existing WebP images'

    def handle(self, *args, **kwargs):
        images_converted = 0

        # 1. 데이터베이스에서 .webp 파일을 제외하고 쿼리
        galleries = Gallery.objects.exclude(head_image__icontains='.webp').iterator()

        for gallery in galleries:
            if gallery.head_image and gallery.head_image.name:
                img_path = gallery.head_image.path

                # 2. 파일 확장자 체크: .webp 파일은 건너뛰기
                if not img_path.lower().endswith(('.jpg', '.png')):
                    continue

                if not os.path.exists(img_path):
                    continue

                try:
                    img = Image.open(img_path)
                    img_dir, img_filename = os.path.split(img_path)
                    img_name, img_ext = os.path.splitext(img_filename)

                    # EXIF 회전 정보 적용 (EXIF 데이터가 있을 때만)
                    if hasattr(img, '_getexif') and img._getexif():
                        img = ImageOps.exif_transpose(img)

                    webp_path = os.path.join(img_dir, f"{img_name}.webp")

                    if img_ext.lower() not in ['.webp']:
                        # WebP로 저장 (method=6은 빠른 속도와 품질 균형)
                        img.save(webp_path, 'WEBP', quality=80, method=6)

                        if os.path.exists(webp_path):
                            # Django 모델 업데이트
                            gallery.head_image.name = os.path.relpath(webp_path, settings.MEDIA_ROOT)
                            gallery.save(update_fields=['head_image'])

                            # 원본 이미지 삭제
                            os.remove(img_path)

                            images_converted += 1
                            self.stdout.write(self.style.SUCCESS(f'Converted {img_path} to {webp_path}'))
                        else:
                            self.stdout.write(self.style.ERROR(f'Failed to save WebP image: {webp_path}'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error processing image {img_path}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Total images converted: {images_converted}'))
