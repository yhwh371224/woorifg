import os
from PIL import Image
from django.core.management.base import BaseCommand
from gallery.models import Gallery
from django.conf import settings


class Command(BaseCommand):
    help = 'Rotate the most recent image by 90 or -90 degrees based on its current orientation'

    def add_arguments(self, parser):
        parser.add_argument(
            'degree', 
            type=int, 
            choices=[90, -90], 
            help='Degree to rotate the image. Use 90 or -90.'
        )

        parser.add_argument(
            'image_id',
            type=int,
            help='ID of the image to rotate.'
        )

    def handle(self, *args, **kwargs):
        degree = kwargs['degree']
        image_id = kwargs['image_id']

        try:
            gallery = Gallery.objects.get(id=image_id)
        except Gallery.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'No image found with ID {image_id}.'))
            return
        
        img_path = gallery.head_image.path
        img_dir, img_filename = os.path.split(img_path)
        img_name, img_ext = os.path.splitext(img_filename)

        with Image.open(img_path) as img:
            img = img.rotate(degree, expand=True)
            img.save(img_path)

        # 모델 업데이트 (이미지 파일이 업데이트 되면 모델에 반영)
        gallery.save(update_fields=['head_image'])
