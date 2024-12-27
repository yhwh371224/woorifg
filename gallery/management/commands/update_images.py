from django.core.management.base import BaseCommand
from PIL import Image, ImageOps
import os
from django.conf import settings
from gallery.models import Gallery


class Command(BaseCommand):
    help = 'Update and rotate existing images, convert to WebP and store in correct directories'

    def handle(self, *args, **kwargs):
        updated_images = 0

        # 모든 Gallery 항목을 순회
        for gallery in Gallery.objects.all():
            if gallery.head_image:
                img_path = gallery.head_image.path
                try:
                    # # 이미지가 존재하고 jpg/png 형식일 때
                    # if img_path.lower().endswith(('jpg', 'jpeg', 'png')) and os.path.exists(img_path):
                    #     img = Image.open(img_path)

                    #     # JPG/PNG 이미지를 WEBP로 변환
                    #     if img.format != 'WEBP':
                    #         webp_path = os.path.splitext(img_path)[0] + '.webp'
                    #         img = ImageOps.exif_transpose(img)  # 회전 정보 적용
                    #         img.save(webp_path, 'WEBP', quality=80)
                    #         # 웹P로 변환된 이미지 경로 설정
                    #         gallery.head_image.name = os.path.relpath(webp_path, settings.MEDIA_ROOT)
                    #         gallery.save()
                    #         os.remove(img_path)
                    #         updated_images += 1
                    #         self.stdout.write(self.style.SUCCESS(f'Converted {img_path} to {webp_path}'))

                    # WEBP 이미지가 이미 있는 경우, 회전 적용 필요
                    if img_path.lower().endswith('webp'):
                        img = Image.open(img_path)
                        img = ImageOps.exif_transpose(img)  # 회전 정보 적용
                        img.save(img_path, 'WEBP', quality=80)  # 기존 경로에 덮어쓰기

                        # 회전 후 저장
                        updated_images += 1
                        self.stdout.write(self.style.SUCCESS(f'Rotated {img_path}'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error processing image {img_path}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Total images updated: {updated_images}'))
