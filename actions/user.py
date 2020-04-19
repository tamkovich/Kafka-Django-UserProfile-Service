import os
# django project name is adleads, replace adleads with your project name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kafka_django.settings")
import django
django.setup()

from web.models import UserProfile
from actions.action import AbstractAction


class ProfileAction(AbstractAction):
    model = UserProfile

    def create(self):
        user_id = self.data.pop('user_id')
        self.model.objects.create(
            user_id=user_id,
            **self.data,
        )

    def _get_instance(self):
        user_id = self.data.pop('user_id')
        return self.model.objects.get(user_id=user_id)
