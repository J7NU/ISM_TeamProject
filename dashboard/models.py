from django.db import models
from django.utils import timezone
from datetime import timedelta
from users import models as user_models

class MLModel(models.Model):
    name = models.CharField(max_length=255)
    model_file = models.FileField(upload_to='models/')

    def __str__(self):
        return self.name

class Warehouse(models.Model):
    warehouse_id = models.BigAutoField(primary_key=True)
    warehouse_name = models.CharField(max_length=100)
    warehouse_latitude = models.CharField(max_length=100)
    warehouse_longitude = models.CharField(max_length=100)
    warehouse_address = models.CharField(max_length=200)
    warehouse_capacity = models.DecimalField(default=0.00, decimal_places=2, max_digits=5)
    # user_id는 users앱의 userDB 모델로 부터 받기
    user = models.ForeignKey(user_models.UserDB, on_delete=models.CASCADE)

    def __str__(self):
        return self.warehouse_name


class Fruit(models.Model):
    fruit_id = models.BigAutoField(primary_key=True)
    fruit_name = models.CharField(max_length=50)
    fruit_day_plus = models.IntegerField(default=0)

    def __str__(self):
        return self.fruit_name


class Origin(models.Model):
    origin_id = models.BigAutoField(primary_key=True)
    origin_location = models.CharField(max_length=200)
    origin_address = models.CharField(max_length=200)
    origin_latitude = models.CharField(max_length=200)
    origin_longitude = models.CharField(max_length=200)


    def __str__(self):
        return self.origin_location


class Barcode(models.Model):
    barcode_id = models.CharField(primary_key=True, max_length=50)
    origin = models.ForeignKey(Origin, on_delete=models.CASCADE)
    fruit = models.ForeignKey(Fruit, on_delete=models.CASCADE)
    user = models.ForeignKey(user_models.UserDB, on_delete=models.CASCADE)

    def __str__(self):
        return self.barcode_id


class Warehousing(models.Model):
    warehousing_id = models.BigAutoField(primary_key=True)
    warehousing_time = models.DateTimeField(default=timezone.now)
    warehousing_quantity = models.IntegerField(default=0)
    warehousing_until = models.DateTimeField(default=timezone.now)
    warehousing_price = models.IntegerField(default=0)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    barcode = models.ForeignKey(Barcode, on_delete=models.CASCADE)
    user = models.ForeignKey(user_models.UserDB, on_delete=models.CASCADE)


class Shipping(models.Model):
    shipping_id = models.BigAutoField(primary_key=True)
    Shipping_time = models.DateTimeField(default=timezone.now)
    Shipping_quantity = models.IntegerField(default=0)
    Shipping_price = models.IntegerField(default=0)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    barcode = models.ForeignKey(Barcode, on_delete=models.CASCADE)
    user = models.ForeignKey(user_models.UserDB, on_delete=models.CASCADE)


class Inventory(models.Model):
    inventory_id = models.BigAutoField(primary_key=True)
    inventory_quantity = models.IntegerField(default=0)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    barcode = models.ForeignKey(Barcode, on_delete=models.CASCADE)
    user = models.ForeignKey(user_models.UserDB, on_delete=models.CASCADE)
