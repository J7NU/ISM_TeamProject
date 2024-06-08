from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .models import Fruit,Origin,Inventory,Warehousing,Shipping,Warehouse, User, Barcode
from .forms import FruitForm,OriginForm,InventoryForm,WarehousingForm,ShippingForm,WarehouseForm, UserForm, BarcodeForm
from django.contrib import messages

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


def warehousing(request):
    inventories = Inventory.objects.all()
    form = WarehousingForm(request.POST or None)
    if form.is_valid():
        form.save()
        redirect('warehousing')
    context = {
        'inventories': inventories,
        'form': form
    }
    return render(request, "warehousing/warehousing.html",context)




def warehousing_edit(request, id):
    warehousings = Warehousing.objects.get(warehousing_id=id)
    form = WarehousingForm(request.POST or None, instance=warehousings)
    if form.is_valid():
        form.save()
        messages.success(request, '입고 정보가 수정되었습니다.')
        return redirect('warehousing')
    return render(request, "warehousing/warehousing_edit.html",{'form':form,'warehousings':warehousings})
def warehouseing_delete(request,id):
    warehousings = Warehousing.objects.get(id=id)
    if request.method == 'POST':
        warehousings.delete()
        return redirect('warehousing')
    return render(request,"warehousing/warehousing_delete_confirm.html")


def shipping(request):
    shippings = Shipping.objects.all()
    context = {
        'shippings': shippings
    }
    return render(request, "shipping/shipping.html",context)


def shipping_edit(request,id):
    shippings = Shipping.objects.get(shipping_id=id)
    form = ShippingForm(request.POST or None, instance=shippings)
    if form.is_valid():
        form.save()
        messages.success(request, '입고 정보가 수정되었습니다.')
        return redirect('shipping')
    return render(request, "shipping/shipping_edit.html",{'form': form, 'shippings':shippings})


def warehouse(request):
    warehouses = Warehouse.objects.all()
    form = WarehouseForm(request.POST or None)
    if form.is_valid():
        form.save()
        redirect('warehouse')
    context = {
        'warehouses': warehouses,
        'form' : form
    }
    return render(request, "warehouse/warehouse.html",context)


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