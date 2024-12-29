import os
from PIL import Image, ImageOps
from django.core.management.base import BaseCommand
from django.conf import settings
from gallery.models import Gallery


class Command(BaseCommand):
    help = 'Convert existing JPG/PNG images to WebP format and rotate existing WebP images'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=1,
            help='Number of recent images to process'
        )

    def handle(self, *args, **kwargs):
        images_converted = 0
        limit = kwargs['limit']  # 사용자 입력값 (기본값: 1)

        # 사용자 입력을 통해 limit 설정
        if not limit:
            try:
                user_input = input("Enter the number of recent images to process (default 5): ").strip()
                limit = int(user_input) if user_input.isdigit() else 5
            except KeyboardInterrupt:
                self.stdout.write(self.style.ERROR("\nOperation cancelled by user."))
                return
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Invalid input: {e}"))
                return
        
        self.stdout.write(self.style.SUCCESS(f'Processing {limit} recent images...'))

        # 1. 최근 limit개의 데이터 중 .webp가 아닌 이미지만 선택
        galleries = (
            Gallery.objects
            .exclude(head_image__icontains='.webp')  # .webp 제외
            .order_by('-id')[:limit]  # 사용자 입력에 따라 제한
        )

        for gallery in galleries:
            if gallery.head_image and gallery.head_image.name:
                img_path = gallery.head_image.path

                if not os.path.exists(img_path):
                    continue

                try:
                    img = Image.open(img_path)
                    img_dir, img_filename = os.path.split(img_path)
                    img_name, img_ext = os.path.splitext(img_filename)

                    # EXIF 회전 정보 적용 (Orientation 태그만 확인)
                    if img.format == 'JPEG' and 'exif' in img.info:
                        exif = img.info.get('exif')  # EXIF 데이터가 있는지 확인

                        if exif:  # EXIF 데이터가 실제로 존재할 경우에만 실행
                            try:
                                exif_data = img.getexif()
                                orientation = exif_data.get(0x0112)  # Orientation 태그 (0x0112)

                                if orientation in [3, 6, 8]:
                                    img = ImageOps.exif_transpose(img)
                            except Exception as e:
                                self.stdout.write(self.style.WARNING(f'Failed to apply EXIF orientation: {e}'))

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
