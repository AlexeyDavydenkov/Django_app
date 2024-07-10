from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.urls import reverse
from .models import Product, Order


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='test_user', password='qwerty')
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.login(username='test_user', password='qwerty')
        self.product = Product.objects.create(
            name='test_product',
            price=125.2,
            description='Product 1',
            discount=10,
            created_by=self.user,
        )
        self.order = Order.objects.create(
            user=self.user,
            delivery_address='Test street, 123',
            promocode='test123'
        )
        self.order.product.set([self.product])

    def tearDown(self):
        self.product.delete()
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(
            reverse('shopapp:order_details', kwargs={'pk': self.order.pk})
        )
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.context['order'].pk, self.order.pk)
        self.assertContains(response, self.product.name)


class OrdersExportTestCase(TestCase):
    fixtures = [
        "users-fixture.json",
        "products-fixture.json",
        "orders-fixture.json",
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.filter(pk=1).first()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        self.client.force_login(self.user)

    def test_get_orders_view(self):
        response = self.client.get(reverse('shopapp:orders_export'), )
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.all()
        expected_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user_pk": order.user.pk,
                "products": [product.pk for product in order.product.all()],
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(
            orders_data["orders"],
            expected_data
        )
