from django.db import models
from core.models import PlantingSeason
class Sale(models.Model):
    season = models.ForeignKey(PlantingSeason, on_delete=models.PROTECT, related_name="sales_sales", null=True, blank=True)
    STATUS=(('LUNAS','Lunas'),('SEBAGIAN','Sebagian'),('BELUM','Belum Lunas'))
    date=models.DateField(); customer=models.CharField(max_length=120); product=models.CharField(max_length=80,default='Gabah')
    quantity_kg=models.DecimalField(max_digits=12,decimal_places=2); price_per_kg=models.DecimalField(max_digits=12,decimal_places=2)
    total_amount=models.DecimalField(max_digits=14,decimal_places=2); status=models.CharField(max_length=10,choices=STATUS,default='BELUM')
    class Meta: ordering=['-date']
