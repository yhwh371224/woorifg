from celery import shared_task
from PIL import Image
import os
from django.conf import settings

@shared_task
def convert_image_to_webp(gallery_id):
    try:
        # 모델을 함수 내에서 지연된 import로 가져옵니다.
        from gallery.models import Gallery
        
        gallery = Gallery.objects.get(id=gallery_id)
        img_path = gallery.head_image.path
        if img_path.lower().endswith(('jpg', 'jpeg', 'png')) and os.path.exists(img_path):
            img = Image.open(img_path)

            webp_path = os.path.splitext(img_path)[0] + '.webp'

            img.save(webp_path, 'WEBP', quality=80)

            gallery.head_image.name = os.path.relpath(webp_path, settings.MEDIA_ROOT)
            gallery.save()

            os.remove(img_path)

            print(f"Converted {img_path} to {webp_path}")
    except Exception as e:
        print(f"Error converting image {gallery_id}: {e}")

