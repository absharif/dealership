from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products, name='products'),

    path('product_category/', views.product_category, name='product_category'),
    path('product_category/add_new/', views.new_product_category, name='new_products_category'),
    path('product_category/edit/', views.edit_product_category, name='edit_products_category'),
    path('product_category/delete/', views.delete_product_category, name='delete_products_category'),

    path('product_transaction/', views.product_transaction, name='product_transaction'),
    path('product_transaction_from_delivery_sheet/', views.product_transaction_from_delivery_sheet,
         name='product_transaction_from_delivery_sheet'),
    path('confirm_product_transaction/', views.confirm_product_transaction, name='confirm_product_transaction'),
    path('product_transaction_confirmed/', views.product_transaction_confirmed, name='product_transaction_confirmed'),
]
