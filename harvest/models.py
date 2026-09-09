from django.db import models
from core.models import PlantingSeason
class Harvest(models.Model):
    season = models.ForeignKey(PlantingSeason, on_delete=models.PROTECT, related_name="harvest_harvests", null=True, blank=True)
    date=models.DateField()
    description=models.CharField(max_length=255)
    quantity_kg=models.DecimalField(max_digits=12,decimal_places=2)
    moisture=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    class Meta: ordering=['-date']
