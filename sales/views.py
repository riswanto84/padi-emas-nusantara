from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.utils import timezone
from core.models import PlantingSeason
from .models import Sale
@login_required
def sale_list(request):
    seasons=PlantingSeason.objects.all(); sid=request.GET.get('season') or request.POST.get('season'); season=seasons.filter(pk=sid).first() if sid else seasons.filter(status='AKTIF').first(); qs=Sale.objects.select_related('season').all(); qs=qs.filter(season=season) if season else qs
    if request.method=='POST':
        try:
            qty=Decimal(request.POST.get('quantity_kg') or 0); price=Decimal(request.POST.get('price_per_kg') or 0); Sale.objects.create(season=season,date=request.POST.get('date') or timezone.localdate(),customer=request.POST.get('customer','').strip(),product=request.POST.get('product','Gabah').strip() or 'Gabah',quantity_kg=qty,price_per_kg=price,total_amount=qty*price,status=request.POST.get('status','BELUM')); messages.success(request,'Penjualan berhasil dicatat.'); return redirect('sale_list')
        except (InvalidOperation,ValueError): messages.error(request,'Data penjualan tidak valid.')
    total = qs.aggregate(v=Sum('total_amount'))['v'] or 0
    qty = qs.aggregate(v=Sum('quantity_kg'))['v'] or 0
    sale_count = qs.count()
    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    page_numbers = paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1)
    return render(request,'sales/sale_list.html',{'sales':page_obj,'page_obj':page_obj,'page_numbers':page_numbers,'seasons':seasons,'season':season,'total':total,'qty':qty,'sale_count':sale_count})
