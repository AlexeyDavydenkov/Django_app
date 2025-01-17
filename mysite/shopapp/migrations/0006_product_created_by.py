# Generated by Django 5.1a1 on 2024-06-25 09:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shopapp", "0005_order_product"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="created_by",
            field=models.ForeignKey(
                default=2,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="created_products",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
