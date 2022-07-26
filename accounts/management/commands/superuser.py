from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Creates Super User'

    def handle(self, *args, **options):
        if not User.objects.filter(username='cryptoAdmin').exists():
            User.objects.create_superuser('cryptoAdmin','Admin1234')
            self.stdout.write(self.style.SUCCESS(f'Successfully Created Super User'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Admin Already Exists! No need to create new one'))

