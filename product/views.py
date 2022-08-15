from django.shortcuts import render
from .models import Product
from django.shortcuts import redirect
from .forms import *
from bin.models import BIN
from order.models import OrderSetting, Order, ItemInOrder
from django.contrib.auth.decorators import login_required


'''
    Product Category Related View

'''


@login_required
def product_category(request):
    try:
        bin = BIN.objects.get(id=request.session['bin'])
    except BIN.DoesNotExist:
        bin = None

    category_list = ProductCategory.objects.filter(bin=bin)
    return render(request, "product/product_category.html", {'category_list': category_list})


@login_required
def new_product_category(request):
    pass


@login_required
def edit_product_category(request):
    pass


@login_required
def delete_product_category(request):
    pass


'''
    Products Related Views
'''


@login_required
def products(request):
    try:
        bin = BIN.objects.get(id=request.session['bin'])
    except BIN.DoesNotExist:
        bin = None

    category_list = ProductCategory.objects.filter(bin=bin)
    product_list = {}
    for category in category_list:
        product_list[category] = Product.objects.filter(bin=bin, category=category)
    return render(request, "product/products.html", {'product_list': product_list, 'category_list': category_list})


@login_required
def product_transaction(request):
    try:
        bin = BIN.objects.get(id=request.session['bin'])
    except BIN.DoesNotExist:
        bin = None

    category_list = ProductCategory.objects.all()
    product_list = {}
    for category in category_list:
        product_list[category] = Product.objects.filter(bin=bin, category=category)

    session_data = {}
    if 'product_transaction' in request.session.keys():
        session_data = request.session['product_transaction']

    if request.method == 'POST':
        selected_product = {}
        for products in product_list.values():
            for product in products:
                if request.POST.get(str(product.id)):
                    selected_product[product.id] = request.POST.get(str(product.id))
        request.session['product_transaction'] = selected_product
        return redirect('confirm_product_transaction')
    return render(request, "product/product_transaction.html", {'product_list': product_list, 'session_data': session_data})


@login_required
def product_transaction_from_delivery_sheet(request):
    product_list = {}
    try:
        bin = BIN.objects.get(id=request.session['bin'])
    except BIN.DoesNotExist:
        bin = None

    try:
        status = OrderSetting.objects.get(bin=bin).default_delivery_sheet_status
    except BIN.DoesNotExist:
        status = None

    if request.method == 'POST':
        form = DeliverySheetForm(data=request.POST)
        if form.is_valid():
            delivery_man = form.cleaned_data['delivery_man']

            try:
                order_list = Order.objects.filter(bin=bin, delivery_man=delivery_man, status=status)
            except Order.DoesNotExist():
                order_list = None

            for order_obj in order_list:
                try:
                    item_list = ItemInOrder.objects.filter(order=order_obj)
                except Order.DoesNotExist():
                    item_list = None

                for item in item_list:
                    if item.product.id in product_list.keys():
                        product_list[item.product.id] += item.quantity
                    else:
                        product_list[item.product.id] = item.quantity

            request.session['product_transaction'] = product_list
            return redirect('confirm_product_transaction')
    else:
        form = DeliverySheetForm()
    return render(request, "order/delivery_sheet.html", {'form': form, 'products': product_list})


@login_required
def confirm_product_transaction(request):
    product_list = {}
    selected_products = {}
    if 'product_transaction' in request.session.keys():
        selected_products = request.session['product_transaction']

    for key, value in selected_products.items():
        try:
            product = Product.objects.get(id=key)
            product_list[product] = value
        except:
            product = None

    if request.method == 'POST':
        form = ProductTransactionForm(data=request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            status = form.cleaned_data['status']
            type = form.cleaned_data['transaction_type']
            remark = form.cleaned_data['remark']
            is_company_transaction = form.cleaned_data['is_company_transaction']

            for product, quantity in product_list.items():
                pt = ProductTransaction()

                pt.product = product
                pt.quantity = quantity
                pt.user = user
                pt.status = status
                pt.transaction_type = type
                pt.remark = remark
                pt.is_company_transaction = is_company_transaction
                pt.save()

            request.session['product_transaction'] = {}
            return redirect('product_transaction_confirmed')

    form = ProductTransactionForm()
    return render(request, "product/confirm_product_transaction.html", {'form': form, 'products': product_list})


@login_required
def product_transaction_confirmed(request):
    return render(request, "product/product_transaction_confirmed.html")

