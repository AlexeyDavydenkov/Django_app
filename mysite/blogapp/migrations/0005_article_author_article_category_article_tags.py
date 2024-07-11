# Generated by Django 5.1a1 on 2024-07-04 09:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blogapp", "0004_article"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="author",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="articles",
                to="blogapp.author",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="article",
            name="category",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="articles",
                to="blogapp.category",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="article",
            name="tags",
            field=models.ManyToManyField(related_name="articles", to="blogapp.tag"),
        ),
    ]