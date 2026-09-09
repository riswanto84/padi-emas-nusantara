from django.contrib import admin
from .models import PlantingSeason
@admin.register(PlantingSeason)
class PlantingSeasonAdmin(admin.ModelAdmin):
    list_display=('name','start_date','end_date','area_ha','target_harvest_kg','status')
    list_filter=('status',)
    search_fields=('name',)
