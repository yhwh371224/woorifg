# gallery/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from gallery.models import Gallery
from .tasks import convert_webp

@receiver(post_save, sender=Gallery)
def convert_webp_after_save(sender, instance, created, **kwargs):

    if created and instance.head_image:
        img_path = instance.head_image.path

        if not img_path.lower().endswith('.webp'):
            print(f"Triggering conversion for image: {img_path}")

            convert_webp.apply_async(args=[instance.id])
        else:
            print(f"{img_path} is already in WebP format, no conversion needed.")
