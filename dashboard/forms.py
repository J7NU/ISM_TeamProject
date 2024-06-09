from django import forms
from .models import Fruit,Origin,Inventory,Warehousing,Shipping,Warehouse, Barcode
from django.contrib.auth.models import User


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
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True)
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['warehouse'].queryset = Warehouse.objects.filter(user=user)

    class Meta:
        model = Warehousing
        fields = ['warehousing_time', 'warehousing_quantity', 'warehousing_price', 'warehouse', 'barcode', 'user']
        widgets = {
            'user': forms.HiddenInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['user'] = self.user
        return cleaned_data




class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ['shipping_price','shipping_quantity','shipping_time',"warehouse",'barcode']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['warehouse'].queryset = Warehouse.objects.filter(user=user)


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['warehouse_address','warehouse_name','warehouse_capacity']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['warehouse'].queryset = Warehouse.objects.filter(user=user)



class BarcodeForm(forms.ModelForm):
    class Meta:
        model = Barcode
        fields = '__all__'

