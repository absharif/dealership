from django.urls import path
from . import views

urlpatterns = [
    path('', views.orders, name='orders'),
    path('<int:id>/', views.order, name='order'),
    path('edit/<int:id>/', views.order_edit, name='order_edit'),
    path('item_edit/<int:id>/', views.order_item_edit, name='order_item_edit'),
    path('delete/<int:id>/', views.order_delete, name='order_delete'),

    path('new_order/', views.new_order, name='new_order'),
    path('confirm_order/', views.confirm_order, name='confirm_order'),
    path('order_confirmed/', views.order_confirmed, name='order_confirmed'),

    path('delivery_sheet/', views.delivery_sheet, name='delivery_sheet'),

    path('payments/', views.payments, name='payments'),
    path('new_payment/', views.new_payment, name='new_payment'),
    path('edit_payment/<int:id>/', views.edit_payment, name='edit_payment'),
]
