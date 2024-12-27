from celery import shared_task
from PIL import Image, ImageOps
import os
from django.conf import settings


@shared_task
def convert_webp(gallery_id):
    try:
        # 모델을 함수 내에서 지연된 import로 가져옴.
        from gallery.models import Gallery
        
        gallery = Gallery.objects.get(id=gallery_id)
        img_path = gallery.head_image.path
        if img_path.lower().endswith(('jpg', 'jpeg', 'png')) and os.path.exists(img_path):
            img = Image.open(img_path)

            # EXIF 회전 정보 적용
            img = ImageOps.exif_transpose(img)

            webp_path = os.path.splitext(img_path)[0] + '.webp'

            img.save(webp_path, 'WEBP', quality=80)

            # 기존 경로에 맞게 저장될 수 있도록 수정
            new_path = os.path.join(settings.MEDIA_ROOT, 'gallery', str(gallery.date.year), 
                                    str(gallery.date.month), str(gallery.date.day), 
                                    os.path.basename(webp_path))
            os.makedirs(os.path.dirname(new_path), exist_ok=True)

            gallery.head_image.name = os.path.relpath(webp_path, settings.MEDIA_ROOT)
            gallery.save()

            os.remove(img_path)

            print(f"Converted {img_path} to {webp_path}")
    except Exception as e:
        print(f"Error converting image {gallery_id}: {e}")

