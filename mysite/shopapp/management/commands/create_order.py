from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Order


class Command(BaseCommand):
    """
    Creates order
    """
    def handle(self, *args, **options):
        self.stdout.write("Create order")
        user =User.objects.get(username="admin")
        order = Order.objects.get_or_create(
            delivery_address="Lenina str, 38/2",
            promocode="start586",
            user=user,
        )
        self.stdout.write(f"Create order {order}")