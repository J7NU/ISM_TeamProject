from django import forms
from .models import Fruit,Origin,Inventory,Warehousing,Shipping,Warehouse, Barcode


class FruitForm(forms.ModelForm):
    class Meta:
        model = Fruit
        fields = '__all__'


class OriginForm(forms.ModelForm):
    class Meta:
        model = Origin
        fields = '__all__'


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'


class WarehousingForm(forms.ModelForm):
    class Meta:
        model = Warehousing
        fields = ['warehousing_time','warehousing_quantity','warehousing_price','warehousing_id','warehouse','user']


class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ['shipping_price','shipping_quantity','shipping_time',"shipping_id"]


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['warehouse_address','warehouse_name','warehouse_capacity','user']




class BarcodeForm(forms.ModelForm):
    class Meta:
        model = Barcode
        fields = '__all__'

