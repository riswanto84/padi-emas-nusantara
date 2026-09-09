from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from core.models import PlantingSeason
from harvest.models import Harvest
from sales.models import Sale
from .models import Expense, TaxProfile, SeasonFinanceProfile

def has_finance_access(user): return user.is_superuser or user.groups.filter(name__in=['Administrator','Manajer','Keuangan']).exists()
def finance_required(view): return login_required(lambda request,*args,**kwargs: view(request,*args,**kwargs) if has_finance_access(request.user) else render(request,'403.html',status=403))
def _selected_season(request):
    seasons=PlantingSeason.objects.all(); sid=request.GET.get('season') or request.POST.get('season'); season=seasons.filter(pk=sid).first() if sid else seasons.filter(status='AKTIF').first(); return seasons,season
@finance_required
def expense_list(request):
    seasons,season=_selected_season(request); qs=Expense.objects.select_related('season').all(); qs=qs.filter(season=season) if season else qs
    if request.method=='POST':
        try:
            Expense.objects.create(season=get_object_or_404(PlantingSeason,pk=request.POST.get('season')) if request.POST.get('season') else season,date=request.POST.get('date') or timezone.localdate(),category=request.POST.get('category','Lainnya').strip(),description=request.POST.get('description','').strip(),amount=Decimal(request.POST.get('amount') or 0)); messages.success(request,'Pengeluaran berhasil dicatat.'); return redirect('expense_list')
        except (InvalidOperation,ValueError): messages.error(request,'Nominal pengeluaran tidak valid.')
    total = qs.aggregate(v=Sum('amount'))['v'] or Decimal('0')
    expense_count = qs.count()
    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    page_numbers = paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1)
    return render(request,'finance/expense_list.html',{'expenses':page_obj,'page_obj':page_obj,'page_numbers':page_numbers,'seasons':seasons,'season':season,'total':total,'expense_count':expense_count})
@finance_required
def gross_turnover_report(request):
    seasons,season=_selected_season(request); sales=Sale.objects.filter(season=season) if season else Sale.objects.all(); total=sales.aggregate(v=Sum('total_amount'))['v'] or Decimal('0'); qty=sales.aggregate(v=Sum('quantity_kg'))['v'] or Decimal('0'); monthly_qs=sales.values('date__year','date__month').annotate(total=Sum('total_amount'),quantity=Sum('quantity_kg')).order_by('-date__year','-date__month'); paginator=Paginator(monthly_qs, 12); page_obj=paginator.get_page(request.GET.get('page')); page_numbers=paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1); return render(request,'finance/gross_turnover_report.html',{'seasons':seasons,'season':season,'sales_total':total,'sales_qty':qty,'average_price':total/qty if qty else Decimal('0'),'sale_count':sales.count(),'monthly':page_obj,'page_obj':page_obj,'page_numbers':page_numbers})
@finance_required
def balance_sheet_report(request):
    seasons,season=_selected_season(request)
    if not season:return render(request,'finance/balance_sheet_report.html',{'seasons':seasons,'season':None,'profile':None,'empty':True})
    profile,_=SeasonFinanceProfile.objects.get_or_create(season=season); expenses=Expense.objects.filter(season=season); harvests=Harvest.objects.filter(season=season); sales=Sale.objects.filter(season=season); expense_total=expenses.aggregate(v=Sum('amount'))['v'] or Decimal('0'); sales_total=sales.aggregate(v=Sum('total_amount'))['v'] or Decimal('0'); harvest_total=harvests.aggregate(v=Sum('quantity_kg'))['v'] or Decimal('0'); sales_qty=sales.aggregate(v=Sum('quantity_kg'))['v'] or Decimal('0'); cost_per_kg=expense_total/harvest_total if harvest_total else Decimal('0'); stock_value=max(harvest_total-sales_qty,Decimal('0'))*cost_per_kg; cash=profile.opening_cash+sales_total-expense_total; total_assets=cash+stock_value+profile.fixed_assets+profile.other_assets; equity=total_assets-profile.liabilities
    if request.method=='POST':
        for field in ['opening_cash','fixed_assets','other_assets','liabilities']:
            try:setattr(profile,field,Decimal(request.POST.get(field) or 0))
            except InvalidOperation: messages.error(request,'Nilai neraca tidak valid.'); return redirect(request.get_full_path())
        profile.note=request.POST.get('note','').strip(); profile.save(); messages.success(request,'Posisi neraca berhasil disimpan.'); return redirect(request.get_full_path())
    return render(request,'finance/balance_sheet_report.html',{'seasons':seasons,'season':season,'profile':profile,'expense_total':expense_total,'sales_total':sales_total,'stock_value':stock_value,'cash':cash,'total_assets':total_assets,'equity':equity,'harvest_total':harvest_total,'sales_qty':sales_qty,'cost_per_kg':cost_per_kg})
@finance_required
def season_report(request, pk):
    season = get_object_or_404(PlantingSeason, pk=pk)
    expenses = Expense.objects.filter(season=season)
    harvests = Harvest.objects.filter(season=season)
    sales = Sale.objects.filter(season=season)
    expense_total = expenses.aggregate(v=Sum('amount'))['v'] or Decimal('0')
    harvest_total = harvests.aggregate(v=Sum('quantity_kg'))['v'] or Decimal('0')
    sales_total = sales.aggregate(v=Sum('total_amount'))['v'] or Decimal('0')
    sales_qty = sales.aggregate(v=Sum('quantity_kg'))['v'] or Decimal('0')
    profit = sales_total - expense_total
    stock_kg = max(harvest_total - sales_qty, Decimal('0'))
    progress = (harvest_total / season.target_harvest_kg * Decimal('100')) if season.target_harvest_kg else Decimal('0')
    return render(request, 'finance/season_report.html', {
        'season': season,
        'expense_total': expense_total,
        'harvest_total': harvest_total,
        'sales_total': sales_total,
        'sales_qty': sales_qty,
        'profit': profit,
        'stock_kg': stock_kg,
        'progress': min(progress, Decimal('100')),
        'expense_count': expenses.count(),
        'harvest_count': harvests.count(),
        'sale_count': sales.count(),
    })
@finance_required
def financial_report(request):
    seasons=PlantingSeason.objects.all(); sid=request.GET.get('season'); season=seasons.filter(pk=sid).first() if sid else seasons.filter(status='AKTIF').first(); expenses=Expense.objects.filter(season=season) if season else Expense.objects.all(); harvests=Harvest.objects.filter(season=season) if season else Harvest.objects.all(); sales=Sale.objects.filter(season=season) if season else Sale.objects.all(); expense_total=expenses.aggregate(v=Sum('amount'))['v'] or Decimal('0'); harvest_total=harvests.aggregate(v=Sum('quantity_kg'))['v'] or Decimal('0'); sales_total=sales.aggregate(v=Sum('total_amount'))['v'] or Decimal('0'); sales_qty=sales.aggregate(v=Sum('quantity_kg'))['v'] or Decimal('0'); profit=sales_total-expense_total; stock_kg=max(harvest_total-sales_qty,Decimal('0')); category_rows=expenses.values('category').annotate(total=Sum('amount')).order_by('-total'); return render(request,'finance/financial_report.html',{'seasons':seasons,'season':season,'expense_total':expense_total,'harvest_total':harvest_total,'sales_total':sales_total,'sales_qty':sales_qty,'profit':profit,'cost_per_kg':expense_total/harvest_total if harvest_total else 0,'sales_per_kg':sales_total/sales_qty if sales_qty else 0,'stock_kg':stock_kg,'expense_count':expenses.count(),'category_rows':category_rows,'sale_count':sales.count()})
@finance_required
def tax_report(request):
    profile=TaxProfile.objects.filter(is_active=True).first() or TaxProfile.objects.create(name='PPh Final/Omzet',rate=Decimal('0.500'),basis='OMZET',is_active=True,note='Sesuaikan dengan status perpajakan usaha.'); seasons,season=_selected_season(request); sales=Sale.objects.filter(season=season) if season else Sale.objects.all(); expenses=Expense.objects.filter(season=season) if season else Expense.objects.all(); omzet=sales.aggregate(v=Sum('total_amount'))['v'] or Decimal('0'); biaya=expenses.aggregate(v=Sum('amount'))['v'] or Decimal('0'); laba=omzet-biaya; basis_amount=omzet if profile.basis=='OMZET' else max(laba,Decimal('0')); estimated_tax=(basis_amount*profile.rate/Decimal('100')).quantize(Decimal('0.01'))
    if request.method=='POST' and request.user.is_superuser:
        try:profile.rate=Decimal(request.POST.get('rate',profile.rate));profile.basis=request.POST.get('basis',profile.basis);profile.note=request.POST.get('note','').strip();profile.save();messages.success(request,'Konfigurasi pajak diperbarui.');return redirect(request.get_full_path())
        except InvalidOperation:messages.error(request,'Tarif pajak tidak valid.')
    return render(request,'finance/tax_report.html',{'seasons':seasons,'season':season,'profile':profile,'omzet':omzet,'biaya':biaya,'laba':laba,'basis_amount':basis_amount,'estimated_tax':estimated_tax})
