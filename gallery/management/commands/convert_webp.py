import os
from PIL import Image
from django.core.management.base import BaseCommand
from django.conf import settings
from gallery.models import Gallery


class Command(BaseCommand):
    help = 'Convert existing JPG/PNG images to WebP format and rotate existing WebP images'

    def handle(self, *args, **kwargs):
        images_converted = 0

        for gallery in Gallery.objects.all():
            if gallery.head_image:
                img_path = gallery.head_image.path  # 실제 이미지 경로 (예: media/gallery/12/28/image.jpg)

                if os.path.exists(img_path):
                    try:
                        img = Image.open(img_path)
                        img_dir, img_filename = os.path.split(img_path)  # 디렉터리와 파일명 분리
                        img_name, img_ext = os.path.splitext(img_filename)  # 파일명과 확장자 분리

                        # WebP 저장 경로 설정 (기존 날짜별 구조 유지)
                        webp_path = os.path.join(img_dir, f"{img_name}.webp")

                        if img.format != 'WEBP':
                            # WebP로 변환
                            img.save(webp_path, 'WEBP', quality=80)

                            # Django 모델에 새로운 이미지 경로 저장
                            gallery.head_image.name = os.path.relpath(webp_path, settings.MEDIA_ROOT)
                            gallery.save()

                            # 원본 이미지 삭제
                            os.remove(img_path)

                            images_converted += 1
                            self.stdout.write(self.style.SUCCESS(f'Converted {img_path} to {webp_path}'))

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error processing image {img_path}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Total images converted: {images_converted}'))

