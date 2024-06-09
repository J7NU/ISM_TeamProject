from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .models import Fruit,Origin,Inventory,Warehousing,Shipping,Warehouse, Barcode,Warehousing_history
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
    warehousing_histories = Warehousing_history.objects.filter(user=user)
    form = WarehousingForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            warehousing = form.save(commit=False)
            warehousing.user = user
            warehousing.save()
            return redirect('warehousing')
    else:
        form = WarehousingForm()

    warehousings = Warehousing.objects.filter(user=user)

    context = {
        'warehousing_histories': warehousing_histories,
        'form': form,
        'warehousings': warehousings
    }
    return render(request, "warehousing/warehousing.html", context)




def warehousing_edit(request,id):
    user_id = request.user.id
    warehousings = Warehousing.objects.get(warehousing_id=id)
    warehouses = Warehouse.objects.filter(user_id = user_id)
    form = WarehousingForm(request.POST or None, instance=warehousings)
    context = {
        'form': form,
        'warehousings': warehousings,
        'warehouses' : warehouses,
        'user_id': user_id
    }
    if form.is_valid():
        form.save()
        return redirect('warehousing')
    return render(request, "warehousing/warehousing_edit.html",context)


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
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.user = request.user
            warehouse.save()
            return redirect('warehouse',warehouse.pk)
    else:
        form = WarehouseForm()
        context ={
            'form':form,
        }
        return render(request, "warehouse/warehouse.html", context)
    # form = WarehouseForm(request.POST or None)
    # if form.is_valid():
    #     form.save()
    #     redirect('warehouse')
    # context = {
    #     'warehouses': warehouses,
    #     'form' : form
    # }



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