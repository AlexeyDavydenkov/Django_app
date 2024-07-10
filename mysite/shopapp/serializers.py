from rest_framework import serializers

from .models import Order, Product


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "pk",
            "user",
            "delivery_address",
            "promocode",
            "product",
            "created_at",
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "pk",
            "name",
            "description",
            "price",
            "discount",
            "archived",
            "created_by",
            "created_at",
        )
