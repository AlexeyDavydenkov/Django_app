from django.core.management import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):
    """
    Creates product
    """
    def handle(self, *args, **options):
        self.stdout.write("Creating products")

        products = [
            ("Apples", "Fresh apples", 150, 10),
            ("Pears", "Fresh pears", 180, 0),
            ("Cherry", "Fresh cherry", 170, 15),
            ("Cherries", "Fresh cherries", 250, 5),
            ("Strawberry", "Fresh strawberry", 300, 0),
        ]
        for product in products:
            product, created = Product.objects.get_or_create(
                name=product[0],
                description=product[1],
                price=product[2],
                discount=product[3],
            )
            self.stdout.write(f"Product {product.name} created")

        self.stdout.write(self.style.SUCCESS("Products created"))