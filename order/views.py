from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import redirect
from bin.models import BIN
from product.models import Product, ProductCategory
from django.contrib.auth.decorators import login_required
from datetime import datetime


@login_required
def orders(request):
    order_list = {}
    submitted = False

    try:
        bin = BIN.objects.get(id=request.session['bin'])
    except BIN.DoesNotExist:
        bin = None

    start_date = datetime.today()
    end_date = datetime.today()
    try:
        order_list = Order.objects.filter(bin=bin)
    except Order.DoesNotExist():
        order_list = None

    if request.method == 'POST':
        submitted = True
        form = OrderFilterForm(data=request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            memo_no = form.cleaned_data['memo_no']
            status = form.cleaned_data['status']
            dsr = form.cleaned_data['dsr']
            delivery_man = form.cleaned_data['delivery_man']

            if not start_date:
                start_date = datetime.today()

            if not end_date:
                end_date = datetime.today()

            order_list = order_list.filter(date__range=[start_date, end_date])
            if memo_no and order_list:
                order_list = order_list.filter(memo_no=memo_no)
            if status and order_list:
                order_list = order_list.filter(status=status)
            if dsr and order_list:
                order_list = order_list.filter(dsr=dsr)
            if delivery_man and order_list:
                order_list = order_list.filter(delivery_man=delivery_man)
    else:
        order_list = order_list.filter(date__range=[start_date, end_date])
        form = OrderFilterForm()
    return render(request, "order/orders.html", {'form': form, 'orders': order_list, 'submitted': submitted})


@login_required
def order(request, id):
    context = {}
    try:
        order_obj = Order.objects.get(id=id)
    except Order.DoesNotExist():
        order_obj = None

    if order_obj:
        try:
            order_items = ItemInOrder.objects.filter(order=order_obj)
        except:
            order_items = None

    context['order_obj'] = order_obj
    context['order_items'] = order_items
    return render(request, "order/order.html", {'context': context})


@login_required
def new_order(request):
    try:
        bin = BIN.objects.get(id=request.session['bin'])
    except BIN.DoesNotExist:
        bin = None

    category_list = ProductCategory.objects.filter(bin=bin)
    product_list = {}
    for category in category_list:
        product_list[category] = Product.objects.filter(bin=bin, category=category)

    session_data = {}
    if 'cart' in request.session.keys():
        session_data = request.session['cart']

    if request.method == 'POST':
        selected_product = {}
        for products in product_list.values():
            for product in products:
                if request.POST.get(str(product.id)):
                    selected_product[product.id] = request.POST.get(str(product.id))
        request.session['cart'] = selected_product
        return redirect('confirm_order')
    return render(request, "order/new_order.html", {'product_list': product_list, 'session_data': session_data})


@login_required
def order_edit(request, id):
    submitted = False
    order_obj = Order.objects.get(id=id)

    if request.method == 'POST':
        submitted = True
        form = EditOrderForm(request.POST, request.FILES, instance=order_obj)
        if form.is_valid():
            memo_no = form.cleaned_data['memo_no']
            outlet = form.cleaned_data['outlet']
            address = form.cleaned_data['address']
            dsr = form.cleaned_data['dsr']
            delivery_man = form.cleaned_data['delivery_man']
            status = form.cleaned_data['status']
            remarks = form.cleaned_data['remarks']

            if order_obj:
                order_obj.memo_no = memo_no
                order_obj.outlet = outlet
                order_obj.address = address
                order_obj.dsr = dsr
                order_obj.delivery_man = delivery_man
                order_obj.status = status
                order_obj.remarks = remarks
                order_obj.save()
                return redirect('order', id=order_obj.id)
    else:
        form = EditOrderForm(request.POST or None, instance=order_obj)
    return render(request, "order/order_edit.html", {'form': form, 'submitted': submitted})


@login_required
def order_delete(request, id):
    return render(request, "order/orders.html",)


@login_required
def order_item_edit(request, id):
    context = {}
    try:
        order_obj = Order.objects.get(id=id)
    except Order.DoesNotExist():
        order_obj = None

    try:
        order_items = ItemInOrder.objects.filter(order=order_obj)
    except ItemInOrder.DoesNotExist():
        order_items = None

    if request.method == 'POST':
        for item in order_items:
            if request.POST.get(str(item.product.id)):
                if item.quantity != request.POST.get(str(item.product.id)):
                    if request.POST.get(str(item.product.id)):
                        item.quantity = request.POST.get(str(item.product.id))
                        item.save()
                    if request.POST.get(str(item.product.id)) == '0':
                        item.delete()
        return redirect('order', order_obj.id)
    return render(request, "order/order_item_edit.html", {'order_items': order_items, 'order': order_obj})


@login_required
def confirm_order(request):
    product_list = {}
    selected_products = {}
    if 'cart' in request.session.keys():
        selected_products = request.session['cart']

    for key, value in selected_products.items():
        try:
            product = Product.objects.get(id=key)
            product_list[product] = value
        except:
            product = None

    if request.method == 'POST':
        form = NewOrderForm(data=request.POST)
        if form.is_valid():
            memo_no = form.cleaned_data['memo_no']
            outlet = form.cleaned_data['outlet']
            address = form.cleaned_data['address']
            dsr = form.cleaned_data['dsr']
            route = form.cleaned_data['route']
            remarks = form.cleaned_data['remarks']

            order_obj = Order()
            order_obj.memo_no = memo_no
            order_obj.outlet = outlet
            order_obj.address = address
            order_obj.remarks = remarks
            if dsr:
                order_obj.dsr = dsr
            else:
                order_obj.dsr = HumanResource.objects.get(hr_id=request.user.username)
            order_obj.save()

            for product, quantity in product_list.items():
                item = ItemInOrder()

                item.order = order_obj
                item.product = product
                item.quantity = quantity
                item.save()
            request.session['cart'] = {}
            return redirect('order_confirmed')

    form = NewOrderForm()
    return render(request, "order/confirm_order.html", {'form': form, 'products': product_list})


@login_required
def order_confirmed(request):
    return render(request, "order/order_confirmed.html")


@login_required
def delivery_sheet(request):
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
                        product_list[item.product.id]['quantity'] += item.quantity
                    else:
                        product_list[item.product.id] = {'quantity': item.quantity, 'product': item.product}
    else:
        form = DeliverySheetForm()
    return render(request, "order/delivery_sheet.html", {'form': form, 'products': product_list})
