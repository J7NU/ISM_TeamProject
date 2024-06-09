
from django.db import models
from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta



class Fruit(models.Model):
    fruit_id = models.BigAutoField(primary_key=True)
    fruit_name = models.CharField(max_length=50)
    fruit_plus_day = models.IntegerField(default=0)



class Origin(models.Model):
    origin_id = models.BigAutoField(primary_key = True)
    origin_location = models.CharField(max_length =200)
    origin_address = models.CharField(max_length = 200)
    origin_longitude = models.CharField(max_length =200)
    origin_latitude = models.CharField(max_length =200)
class Barcode(models.Model):
    barcode_id = models.BigAutoField(primary_key=True)
    origin = models.ForeignKey(Origin, on_delete=models.CASCADE, db_column='origin_id')
    fruit = models.ForeignKey(Fruit, on_delete=models.CASCADE, db_column='fruit_id')

    # def __str__(self):
    #     return self.barcode_id

class Warehouse(models.Model):
    warehouse_id = models.BigAutoField(primary_key=True)
    warehouse_name = models.CharField(max_length = 100)
    warehouse_longitude = models.CharField(max_length= 100)
    warehouse_latitude = models.CharField(max_length=100)
    warehouse_address = models.CharField(max_length = 200)
    warehouse_capacity = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, db_column='user_id')
    def __str__(self):
        return self.warehouse_name




class Warehousing(models.Model):
    warehousing_id = models.BigAutoField(primary_key=True)
    warehousing_time = models.DateTimeField(default=timezone.now)
    warehousing_quantity = models.IntegerField(default=0)
    warehousing_until = models.DateTimeField(default=timezone.now)
    warehousing_price = models.IntegerField(default=0)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, db_column='warehouse_id')
    barcode = models.ForeignKey(Barcode, on_delete=models.CASCADE, db_column='barcode_id')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user_id')
    def put_warehousing_until(self):
        if self.barcode.fruit.fruit_plus_day:
            self.warehousing_until = self.warehousing_time + timedelta(days=self.barcode.fruit.fruit_plus_day)
        else:
            self.warehousing_until = self.warehousing_time
        return self.warehousing_until



class Inventory(models.Model):
    inventory_id = models.BigAutoField(primary_key=True)
    inventory_quantity = models.IntegerField(default=0)
    warehousing = models.ForeignKey(Warehousing,on_delete=models.CASCADE,db_column = 'warehousing_id')
    inventory_expiration = models.DateField(default= timezone.now)
    warehouse = models.ForeignKey(Warehouse,on_delete=models.CASCADE,db_column='warehouse_id')
    fruit = models.ForeignKey(Fruit, on_delete=models.CASCADE,db_column='fruit_id')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user_id')
    # def put_expiration(self):
    #   self.inventory_expiration = datetime.now().date() + timedelta(days=self.fruit.id.fruit_day_plus)



class Shipping(models.Model):
    shipping_id = models.BigAutoField(primary_key=True)
    shipping_time = models.DateTimeField(default = timezone.now)
    shipping_quantity = models.IntegerField(default = 0)
    shipping_price = models.IntegerField(default=0)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, db_column='warehouse_id')
    barcode = models.ForeignKey(Barcode,on_delete=models.CASCADE,db_column='barcode_id')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user_id')





# Create your models here.
