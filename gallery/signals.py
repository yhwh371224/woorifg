# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Gallery
# from .tasks import convert_webp
# import os
# import logging


# logger = logging.getLogger(__name__)

# @receiver(post_save, sender=Gallery)
# def async_convert_webp(sender, instance, created, **kwargs):
#     if created and instance.head_image:
#         img_path = instance.head_image.name

#         if not img_path.lower().endswith('.webp'):            
#             convert_webp.delay(instance.id)
        
#         else:
#             logger.info(f"{img_path} is already in WebP format, no conversion needed.")
