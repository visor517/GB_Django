from django.core.management import BaseCommand
from users.models import User, UserExtention


class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in User.objects.all():
            UserExtention.objects.create(user=user)
