from django.core.management import BaseCommand
from users.models import User, UserProfile


class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in User.objects.all():
            UserProfile.objects.create(user=user)
