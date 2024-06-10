from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Fruit,Origin,Inventory,Warehousing,Shipping,Warehouse, Barcode
from .forms import FruitForm,OriginForm,InventoryForm,WarehousingForm,ShippingForm,WarehouseForm, BarcodeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
    inventories = Inventory.objects.all()
    context = {
        'inventories': inventories
    }
    return render(request, 'inventory/inventory_summary.html',context)


def inventory_details(request):
    inventories = Inventory.objects.get(id=id)
    form = InventoryForm(request.POST or None, instance = inventories)
    return render(request, 'inventory/inventory_item_detail.html',{'form': form})


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


def warehouseing_delete(request,id):
    warehousings = Warehousing.objects.get(id=id)
    if request.method == 'POST':
        warehousings.delete()
        return redirect('warehousing')
    return render(request,"warehousing/warehousing_delete_confirm.html")

@login_required
def shipping(request):
    user = request.user
    form = ShippingForm(user, request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.user = user
            shipping.save()
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


def warehouse(request):

    if request.method == 'POST':
        form = WarehouseForm(request.user,request.POST)
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.user = request.user
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



def warehouse_detail(request):
    warehouses = Warehouse.objects.get(id=id)
    form = WarehouseForm(request.POST or None, instance=warehouses)
    return render(request, "warehouse/warehouse_detail.html", {'form': form,'warehouse': warehouses})


def warehouse_edit(request):
    warehouses = Warehouse.objects.get(id=id)
    form = WarehouseForm(request.POST or None, instance = warehouses)
    if form.is_valid():
        form.save()
        return redirect('warehouse')
    return render(request, "warehouse/warehouse_detail_edit.html")

def warehouse_delete(request):
    warehouses = Warehouse.objects.get(id=id)
    if request.method == 'POST':
        warehouses.delete()
        return redirect('warehouse')
    return render(request, "warehouse/warehouse_delete_confirm.html")


def recommend(request):
    return render(request, "recommend/recommend_main.html")


def recommend_detail(request):
    return render(request, "recommend/recommend_detail.html")