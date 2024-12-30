# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from gallery.models import Gallery
# from .tasks import convert_webp
# import os
# import logging


# logger = logging.getLogger(__name__)

# @receiver(post_save, sender=Gallery)
# def convert_webp_after_save(sender, instance, created, **kwargs):
#     if created and instance.head_image:
#         img_path = instance.head_image.name

#         if not img_path.lower().endswith('.webp'):
#             if instance.head_image and instance.head_image.path and os.path.exists(instance.head_image.path):
#                 convert_webp.apply_async(args=[instance.id])
#             else:
#                 logger.warning(f"Image file not found: {img_path}")
#         else:
#             logger.info(f"{img_path} is already in WebP format, no conversion needed.")
