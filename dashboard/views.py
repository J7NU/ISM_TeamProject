from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Fruit,Origin,Inventory,Warehousing,Shipping,Warehouse, Barcode
from .forms import FruitForm,OriginForm,InventoryForm,WarehousingForm,ShippingForm,WarehouseForm, BarcodeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver

from .api import kamis

def index(request):
    # 메인 페이지
    print('접속 중....')
    # 데이터 가져오기...
    retail_price = kamis.data_for_graph()
    print("소매 데이터 가져오기 성공")
    print(retail_price)

    temp = loader.get_template('index.html')
    context = {
        "retail_price": retail_price[1],
        "retail_date": retail_price[0]
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
    return render(request, 'product/product_setting.html')


def product_edit(request):
    return render(request, "product/product_edit.html")



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
@receiver(post_save, sender=Warehousing)
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


@receiver(post_save, sender=Shipping)
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


def warehouse_edit(request):
    warehouses = Warehouse.objects.get(id=id)
    form = WarehouseForm(request.POST or None, instance = warehouses)
    if form.is_valid():
        form.save()
        return redirect('warehouse')
    return render(request, "warehouse/warehouse_detail_edit.html")

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