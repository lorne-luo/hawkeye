from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = 'Create default group, superuser, topics and sectors.'

    def handle(self, *args, **options):
        User = get_user_model()
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            admin = User.objects.create_superuser(email='dev@luotao.net',
                                                  password='Luotao123',
                                                  first_name='Tao',
                                                  last_name='Luo')
        self.stdout.write(self.style.SUCCESS('Superuser and contributor group created.'))
