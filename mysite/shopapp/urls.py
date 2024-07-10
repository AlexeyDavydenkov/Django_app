from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    shop_index,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    UpdateProductView,
    ProductDeleteView,
    OrderListView,
    OrderCreateView,
    OrderDetailView,
    UpdateOrderView,
    OrderDeleteView,
    OrderDataExportView,
    ProductViewSet,
    OrderViewSet,
    LatestProductsFeed,
    UserOrdersListView,
    UserOrderExportView,
)

app_name = "shopapp"

router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("", shop_index, name="index"),
    path("api/", include(router.urls)),
    path("products/", ProductListView.as_view(), name="products_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", UpdateProductView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="product_delete"),
    path("products/latest/feed/", LatestProductsFeed(), name="products-feed"),
    path("orders/", OrderListView.as_view(), name="orders_list"),
    path("orders/export/", OrderDataExportView.as_view(), name="orders_export"),
    path("users/<int:user_id>/orders/export/", UserOrderExportView.as_view(), name="user_orders_export"),
    path("orders/create/", OrderCreateView.as_view(), name="create_order"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_details"),
    path("orders/<int:pk>/update/", UpdateOrderView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path("users/<int:user_id>/orders/", UserOrdersListView.as_view(), name="user_orders"),
]
