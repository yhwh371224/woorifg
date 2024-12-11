from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import AnonymousUser
from blog.models import Members


class MembersEmailBackend(BaseBackend):
    def authenticate(self, request, email=None, **kwargs):
        try:
            return Members.objects.get(email=email)
        except Members.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Members.objects.get(pk=user_id)
        except Members.DoesNotExist:
            return None