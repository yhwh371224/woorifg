# import os
# from django.conf import settings
# from PIL import Image, ImageOps
# from celery import shared_task
# from gallery.models import Gallery
# import logging

# logger = logging.getLogger(__name__)

# @shared_task
# def convert_webp(gallery_id):
#     try:
#         gallery = Gallery.objects.get(id=gallery_id)
#         img_path = gallery.head_image.path

#         if img_path.lower().endswith(('jpg', 'jpeg', 'png')) and os.path.exists(img_path):
#             img = Image.open(img_path)

#             # EXIF 회전 정보 적용
#             img = ImageOps.exif_transpose(img)

#             # WebP 형식으로 저장할 새로운 경로 계산
#             webp_path = os.path.splitext(img_path)[0] + '.webp'

#             # WebP 파일로 저장
#             img.save(webp_path, 'WEBP', quality=80)

#             # 새 파일의 저장 경로를 MEDIA_ROOT 기준으로 수정
#             new_path = os.path.join(settings.MEDIA_ROOT, 'gallery', str(gallery.date.year),
#                                     str(gallery.date.month), str(gallery.date.day),
#                                     os.path.basename(webp_path))

#             os.makedirs(os.path.dirname(new_path), exist_ok=True)

#             gallery.head_image.name = os.path.relpath(new_path, settings.MEDIA_ROOT)
#             gallery.save()

#             os.remove(img_path)

#             logger.info(f"Converted {img_path} to {new_path}")

#     except Exception as e:
#         logger.error(f"Error converting image {gallery_id}: {e}", exc_info=True)
