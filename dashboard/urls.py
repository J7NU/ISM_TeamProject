from django.urls import path
from dashboard import views

urlpatterns = [
    path("", views.index, name="index"),
    path("inventory", views.inventory, name="inventory"),
    path("inventory/1", views.inventory_details, name='inventory-item'),
    path("product", views.product_setting, name='product-setting'),
    path("product/edit/1", views.product_edit, name='product-edit'),
    path("warehousing", views.warehousing, name='warehousing'),
    path("warehousing/edit/<int:warehousing_id>", views.warehousing_edit, name="warehousing_edit"),
    path("warehousing/delete/<int:warehousing_id>",views.warehouseing_delete,name="delete_warehousing"),

    path("shipping", views.shipping, name="shipping"),
    path("shipping/edit/<int:shipping_id>", views.shipping_edit, name="shipping_edit"),
    path("shipping/delete/<int:shipping_id>",views.shipping_delete,name="delete_shipping"),
    
    path("warehouse", views.warehouse, name="warehouse"),
    path("warehouse/<int:id>", views.warehouse_detail, name="warehouse_detail"),
    path("warehouse/edit/<int:id>", views.warehouse_edit, name="warehouse_edit"),
    path("warehouse/delete/<int:warehouse_id>",views.warehouse_delete,name="delete_warehouse"),
    
    path("recommend", views.recommend, name="recommend"),
    path("recommend/detail/1", views.recommend_detail, name="recommend_detail"),
]