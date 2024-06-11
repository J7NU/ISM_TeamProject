from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Fruit,Origin,Inventory,Warehousing,Shipping,Warehouse, Barcode
from .forms import FruitForm,OriginForm,InventoryForm,WarehousingForm,ShippingForm,WarehouseForm, BarcodeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta


from .api import kamis

def index(request):
    # 메인 페이지
    print('접속 중....')
    # 데이터 가져오기...
    retail_price = kamis.data_for_graph()
    print("소매 데이터 가져오기 성공")
    print(retail_price)
    inventories = Inventory.objects.filter(user = request.user)
    temp = loader.get_template('index.html')
    context = {
        "retail_price": retail_price[1],
        "retail_date": retail_price[0],
        'inventories':inventories,
    }
    return HttpResponse(temp.render(context, request))


def inventory(request):
    inventories = Inventory.objects.filter(user = request.user)
    context = {
        'inventories': inventories
    }
    return render(request, 'inventory/inventory_summary.html',context)


def inventory_details(request,inventory_id):
    inventories = Inventory.objects.get(inventory_id=inventory_id,user = request.user)
    return render(request, 'inventory/inventory_item_detail.html',{'inventories': inventories})


def product_setting(request):
    user = request.user
    form = BarcodeForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            barcode = form.save(commit=False)
            barcode.user = user
            barcode.save()
            return redirect('product_setting')

    fruits = Fruit.objects.all()
    barcodes = Barcode.objects.filter(user=user)
    origins = Origin.objects.all()
    context = {
        'form': form,
        'barcodes': barcodes,
        'fruits': fruits,
        'origins': origins
    }
    return render(request, 'product/product_setting.html', context)

def product_delete(request,barcode_id):
    user = request.user
    barcodes = Barcode.objects.get(barcode_id=barcode_id, user=user)
    if request.method == 'POST':
        barcodes.delete()
        return redirect('product_setting')
    return render(request, "product/product_delete_confirm.html", {'barcodes': barcodes, 'user': user})

# dashboard/views.py

def product_edit(request, barcode_id):
    barcode = get_object_or_404(Barcode, barcode_id=barcode_id)

    if request.method == 'POST':
        form = BarcodeForm(request.POST, instance=barcode)
        if form.is_valid():
            form.save()
            return redirect('product_setting')
    else:
        form = BarcodeForm(instance=barcode)

    fruits = Fruit.objects.all()
    origins = Origin.objects.all()

    context = {
        'form': form,
        'fruits': fruits,
        'origins': origins,
    }
    return render(request, 'product/product_edit.html', context)

def origin_setting(request):
    form = OriginForm(request.POST or None)
    origins = Origin.objects.all()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('origin_setting')
    return render(request, 'origin/origin_setting.html', {'form':form,'origins':origins})

def origin_delete(request,origin_id):
    origins = Origin.objects.get(origin_id=origin_id)
    if request.method == 'POST':
        origins.delete()
        return redirect('origin_setting')
    return render(request, "origin/origin_delete_confirm.html", {'origins': origins})

# dashboard/views.py

def origin_edit(request, origin_id):
    origins = get_object_or_404(Origin, origin_id=origin_id)
    if request.method == 'POST':
        form = OriginForm(request.POST, instance=origins)
        if form.is_valid():
            form.save()
            return redirect('origin_setting')
    else:
        form = OriginForm(instance=origins)
    return render(request, 'origin/origin_edit.html', {'form':form,'origins':origins})






@login_required
def warehousing(request):
    user = request.user
    form = WarehousingForm(user, request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            warehousing = form.save(commit=False)
            warehousing.user = user
            warehousing.save()
            plus_inventory(warehousing)
            put_warehousing_until(warehousing)
            return redirect('warehousing')
    else:
        form = WarehousingForm(user)

    warehousings = Warehousing.objects.filter(user=user)
    warehouses = Warehouse.objects.filter(user=user)
    context = {
        'form': form,
        'warehousings': warehousings,
        'warehouses': warehouses
    }
    return render(request, "warehousing/warehousing.html", context)



def warehousing_edit(request, warehousing_id):
    user = request.user
    try:
        warehousing = Warehousing.objects.get(warehousing_id=warehousing_id, user=user)
    except Warehousing.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':
        form = WarehousingForm(user, request.POST, instance=warehousing)
        if form.is_valid():
            form.save()
            return redirect('warehousing')
    else:
        form = WarehousingForm(user, instance=warehousing, initial={'warehousing_id': warehousing.warehousing_id})

    warehousings = Warehousing.objects.filter(user=user)
    warehouses = Warehouse.objects.filter(user=user)
    context = {
        'form': form,
        'warehousings': warehousings,
        'warehouses': warehouses
    }
    return render(request, 'warehousing/warehousing_edit.html', context)


def warehouseing_delete(request,warehousing_id):
    user = request.user
    warehousings = Warehousing.objects.get(warehousing_id=warehousing_id, user=user)
    if request.method == 'POST':
        warehousings.delete()
        return redirect('warehousing')
    return render(request,"warehousing/warehousing_delete_confirm.html",{'warehousings':warehousings,'user':user})

@login_required
def shipping(request):
    user = request.user
    form = ShippingForm(user, request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.user = user
            shipping.save()
            minus_inventory(shipping)
            return redirect('shipping')
    else:
        form = ShippingForm(user)
    shippings = Shipping.objects.filter(user=user)
    warehouses = Warehouse.objects.filter(user=user)
    context = {
        'form': form,
        'shippings': shippings,
        'warehouses': warehouses
    }
    return render(request, "shipping/shipping.html", context)

def plus_inventory(instance, **kwargs):
    try:
        inventory = Inventory.objects.get(
            warehouse=instance.warehouse,
            barcode=instance.barcode,
            user=instance.user
        )
        inventory.inventory_quantity += instance.warehousing_quantity
        inventory.save()
    except Inventory.DoesNotExist:
        Inventory.objects.create(
            warehouse=instance.warehouse,
            barcode=instance.barcode,
            user=instance.user,
            inventory_quantity=instance.warehousing_quantity
        )


def minus_inventory(instance, **kwargs):
    try:
        inventory = Inventory.objects.get(
            warehouse=instance.warehouse,
            barcode=instance.barcode,
            user=instance.user
        )
        if inventory.inventory_quantity >= instance.shipping_quantity:
            inventory.inventory_quantity -= instance.shipping_quantity
            inventory.save()
        else:
            raise ValueError(f"재고가 부족합니다. 현재 재고: {inventory.inventory_quantity}, 출고 수량: {instance.shipping_quantity}")
    except Inventory.DoesNotExist:
        raise ValueError("재고 정보가 존재하지 않습니다.")
def put_warehousing_until(instance,**kwargs):
    instance.warehousing_until = instance.warehousing_time + timedelta(days = instance.barcode.fruit.fruit_plus_day)
    instance.save()




def shipping_edit(request,shipping_id):
    user = request.user
    try:
        shipping = Shipping.objects.get(shipping_id =shipping_id, user=user)
    except Shipping.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':
        form = ShippingForm(user, request.POST, instance=shipping)
        if form.is_valid():
            form.save()
            return redirect('shipping')
    else:
        form = ShippingForm(user, instance=shipping, initial={'shipping_id': shipping.shipping_id})

    shippings = Shipping.objects.filter(user=user)
    warehouses = Warehouse.objects.filter(user=user)
    context = {
        'form': form,
        'shippings': shippings,
        'warehouses': warehouses
    }
    return render(request, 'shipping/shipping_edit.html', context)

def shipping_delete(request,shipping_id):
    user = request.user
    shippings = Shipping.objects.get(shipping_id=shipping_id, user=user)
    if request.method == 'POST':
        shippings.delete()
        return redirect('shipping')
    return render(request,"shipping/shipping_delete_confirm.html",{'shippings':shippings,'user':user})



def warehouse(request):

    if request.method == 'POST':
        form = WarehouseForm(request.user,request.POST)
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.user = request.user.id
            warehouse.save()
            return redirect('warehouse')
    else:
        user = request.user
        form = WarehouseForm(user)
        warehouses = Warehouse.objects.filter(user_id = user)
        context ={
            'form':form,
            'warehouses':warehouses
        }
        return render(request, "warehouse/warehouse.html", context)



def warehouse_detail(request,warehouse_id):
    warehouses = Warehouse.objects.get(warehouse_id=warehouse_id)
    warehousings = Warehousing.objects.filter(user_id = request.user,warehouse_id = warehouse_id)
    context = {
        'warehouse': warehouses,
        'warehousings' : warehousings
    }
    return render(request, "warehouse/warehouse_detail.html", context)


def warehouse_edit(request,warehouse_id):
    user = request.user
    try:
        warehouse = Warehouse.objects.get(warehouse_id=warehouse_id, user=user)
    except Warehouse.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':
        form = WarehouseForm(user, request.POST, instance=warehouse)
        if form.is_valid():
            form.save()
            return redirect('warehouse')
    else:
        form = WarehouseForm(user, instance=warehouse, initial={'warehouse_id': warehouse.warehouse_id})
    warehouses = Warehouse.objects.filter(user=user)
    context = {
        'form': form,
        'warehouses': warehouses,
    }
    return render(request, 'warehouse/warehouse_detail_edit.html', context)
    # warehouses = Warehouse.objects.get(warehouse_id=warehouse_id)
    # form = WarehouseForm(request.POST or None, instance = warehouses)
    # if form.is_valid():
    #     form.save()
    #     return redirect('warehouse')
    # return render(request, "warehouse/warehouse_detail_edit.html")

def warehouse_delete(request,warehouse_id):
    user = request.user
    Warehouses = Warehouse.objects.get(warehouse_id=warehouse_id, user=user)
    if request.method == 'POST':
        Warehouses.delete()
        return redirect('warehousing')
    return render(request, "warehousing/warehousing_delete_confirm.html", {'Warehouses': Warehouses, 'user': user})


def recommend(request):
    return render(request, "recommend/recommend_main.html")


def recommend_detail(request):
    return render(request, "recommend/recommend_detail.html")