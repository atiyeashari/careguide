from django.core.management.base import BaseCommand, CommandError

from booking.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        u1 = User(username='u1', password='useruseruser', email='u1@example.com', first_name='u1', last_name='l1')
        u1.save()
        bs1 = BabySitter(user=u1, phone_number='1234567890')
        bs1.save()
        u2 = User(username='u2', password='useruseruser', email='u2@example.com', first_name='u2', last_name='l2')
        u2.save()
        f1 = Family(user=u2, phone_number='1234567890')
        f1.save()