import logging
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Order
from .forms import ProductForm
from .serializers import OrderSerializer, ProductSerializer

log = logging.getLogger(__name__)


def shop_index(request: HttpRequest):
    log.info("Rendering shop index page")
    return render(request, "shopapp/shop-index.html")


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]
    search_fields = [
        'name',
        'description',
    ]
    ordering_fields = [
        "pk",
        "name",
        "price",
    ]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = [
        'user',
        'product',
        'delivery_address',
    ]
    ordering_fields = [
        "pk",
        "user",
    ]


class ProductListView(ListView):
    template_name = "shopapp/products-list.html"
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


class ProductDetailView(DetailView):
    template_name = "shopapp/product-details.html"
    model = Product
    context_object_name = "product"


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "shopapp.add_product"
    model = Product
    form_class = ProductForm
    # fields = "name", "price", "description", "discount"
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class LatestProductsFeed(Feed):
    title = "Shop Latest Products"
    description = "Shop Latest Products"
    link = reverse_lazy("shopapp:products_list")

    def items(self):
        return Product.objects.filter(archived=False).order_by("-created_at")[:20]

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:100]


class UpdateProductView(UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    # fields = "name", "price", "description", "discount"
    template_name_suffix = "_update_form"

    def test_func(self):
        if self.request.user.is_superuser:
            return True

        self.object = self.get_object()
        has_edit_perm = self.request.user.has_perm("shopapp.change_product")
        created_by_current_user = self.object.created_by == self.request.user
        return has_edit_perm and created_by_current_user

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderListView(ListView):
    queryset = Order.objects.select_related("user").prefetch_related("product")


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = Order.objects.select_related("user").prefetch_related("product")


class OrderCreateView(CreateView):
    model = Order
    fields = "product", "user", "delivery_address", "promocode"
    success_url = reverse_lazy("shopapp:orders_list")


class UpdateOrderView(UpdateView):
    model = Order
    fields = "product", "user", "delivery_address", "promocode"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk},
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")


class OrderDataExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.all()
        orders_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user_pk": order.user.pk,
                "products": [product.pk for product in order.product.all()],
            }
            for order in orders
        ]
        print(3 + 4)
        return JsonResponse({"orders": orders_data})


class UserOrdersListView(ListView):
    template_name = 'shopapp/user_orders.html'
    context_object_name = 'user_orders'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Order.objects.filter(user_id=user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['user_id']
        user = User.objects.get(pk=user_id)
        context['owner'] = user
        return context


class UserOrderExportView(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        cache_key = f'user_orders_{user_id}'
        orders_data = cache.get(cache_key)
        if not orders_data:
            orders = Order.objects.filter(user=user).order_by('pk')
            serializer = OrderSerializer(orders, many=True)
            orders_data = serializer.data
            cache.set(cache_key, orders_data, 300)
        return JsonResponse({f"Orders {user.username}": orders_data})
