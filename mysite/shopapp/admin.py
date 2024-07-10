from io import TextIOWrapper
from csv import DictReader

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib.auth.models import User

from .models import Product, Order
from .forms import SCVImportForm


class OrderInline(admin.TabularInline):
    model = Product.orders.through
    extra = 0


@admin.action(description="Archive products")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description="Unarchive products")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [
        mark_archived,
        mark_unarchived,
    ]
    inlines = [
        OrderInline,
    ]
    list_display = "pk", "name", "description_short", "price", "discount", "archived"
    list_display_links = "pk", "name"
    ordering = "pk",
    search_fields = "name", "description", "price"
    fieldsets = [
        (None, {"fields": ("name", "description")}),
        ("Price options", {"fields": ("price", "discount")}),
        ("Additional options", {"fields": ("archived",), "classes": ("collapse",)}),
    ]

    def description_short(self, object: Product) -> str:
        if len(object.description) < 48:
            return object.description
        return object.description[:48] + "..."

    description_short.short_description = "My Custom Field"


class ProductInline(admin.StackedInline):
    model = Order.product.through
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = "shopapp/orders_changelist.html"
    inlines = [
        ProductInline,
    ]
    list_display = "pk", "user", "delivery_address", "promocode"
    list_display_links = "pk", "user"
    ordering = "pk",
    search_fields = "pk", "promocode"

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("product")

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = SCVImportForm()
            context = {"form": form}
            return render(request, "admin/csv_form.html", context)
        form = SCVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {"form": form}
            return render(request, "admin/csv_form.html", context, status=400)
        csv_file = TextIOWrapper(
            form.files["csv_file"].file, encoding=request.encoding,
        )
        reader = DictReader(csv_file)

        orders = []
        for row in reader:
            try:
                user = User.objects.get(username=row["user"])
                products = []
                for product_name in row["product"].split(','):
                    try:
                        product = Product.objects.get(name=product_name.strip())
                        products.append(product)
                    except Product.DoesNotExist:
                        self.message_user(request, f"Product {product_name} does not exist.", level="error")
                        continue

                if products:
                    order = Order(
                        user=user,
                        delivery_address=row["delivery_address"],
                        promocode=row["promocode"]
                    )
                    order.save()
                    order.product.set(products)
                    orders.append(order)
            except User.DoesNotExist:
                self.message_user(request, f"User {row['user']} does not exist.", level="error")
                continue

        if orders:
            self.message_user(request, "Successfully imported CSV file")
        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("import-orders-csv/", self.import_csv, name="import-orders-csv"),
        ]
        return new_urls + urls
