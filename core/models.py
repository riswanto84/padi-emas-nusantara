from django.db import models

class PlantingSeason(models.Model):
    STATUS_CHOICES = [('DRAFT','Draft'),('AKTIF','Aktif'),('SELESAI','Selesai')]
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    area_ha = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    target_harvest_kg = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-start_date']
    def __str__(self): return self.name
