from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from core.models import PlantingSeason
from .models import Harvest
@login_required
def harvest_list(request):
    seasons=PlantingSeason.objects.all(); sid=request.GET.get('season') or request.POST.get('season'); season=seasons.filter(pk=sid).first() if sid else seasons.filter(status='AKTIF').first(); qs=Harvest.objects.select_related('season').all(); qs=qs.filter(season=season) if season else qs
    if request.method=='POST':
        try: Harvest.objects.create(season=season,date=request.POST.get('date') or timezone.localdate(),description=request.POST.get('description','').strip(),quantity_kg=Decimal(request.POST.get('quantity_kg') or 0),moisture=Decimal(request.POST['moisture']) if request.POST.get('moisture') else None); messages.success(request,'Hasil panen berhasil dicatat.'); return redirect('harvest_list')
        except (InvalidOperation,ValueError): messages.error(request,'Data panen tidak valid.')
    total = qs.aggregate(v=Sum('quantity_kg'))['v'] or 0
    harvest_count = qs.count()
    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    page_numbers = paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1)
    return render(request,'harvest/harvest_list.html',{'harvests':page_obj,'page_obj':page_obj,'page_numbers':page_numbers,'seasons':seasons,'season':season,'total':total,'harvest_count':harvest_count})
