from decimal import Decimal
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.db.models import Sum
from django.http import HttpResponse
from django.utils import timezone

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, Image as RLImage,
)

from core.models import PlantingSeason
from harvest.models import Harvest
from sales.models import Sale
from .models import Expense, TaxProfile, SeasonFinanceProfile
from .views import finance_required

GREEN = colors.HexColor('#087443')
DARK = colors.HexColor('#183a2b')
MID = colors.HexColor('#5f776b')
LIGHT = colors.HexColor('#edf7f0')
BORDER = colors.HexColor('#d7e6dc')
GOLD = colors.HexColor('#d8aa2c')
RED = colors.HexColor('#b64a4a')


def money(value):
    try:
        n = Decimal(str(value or 0))
    except Exception:
        n = Decimal('0')
    return 'Rp {:,.0f}'.format(n).replace(',', '.')


def number(value):
    try:
        n = Decimal(str(value or 0))
    except Exception:
        n = Decimal('0')
    return '{:,.0f}'.format(n).replace(',', '.')


def pct(value):
    try:
        return '{:,.1f}%'.format(Decimal(str(value or 0))).replace(',', 'X').replace('.', ',').replace('X', '.')
    except Exception:
        return '0,0%'


def para(text, style):
    return Paragraph(str(text), style)


class NumberedDocTemplate(BaseDocTemplate):
    def __init__(self, *args, logo_path=None, report_title='', season_label='', **kwargs):
        self.logo_path = logo_path
        self.report_title = report_title
        self.season_label = season_label
        super().__init__(*args, **kwargs)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id='normal')
        self.addPageTemplates([PageTemplate(id='main', frames=frame, onPage=self._draw_header_footer)])

    def _draw_header_footer(self, canvas, doc):
        canvas.saveState()
        width, height = A4
        # Header / letterhead
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.8)
        canvas.line(18 * mm, height - 31 * mm, width - 18 * mm, height - 31 * mm)
        if self.logo_path and Path(self.logo_path).exists():
            try:
                canvas.drawImage(self.logo_path, 18 * mm, height - 28 * mm, width=58 * mm, height=17.5 * mm,
                                 preserveAspectRatio=True, mask='auto', anchor='sw')
            except Exception:
                pass
        canvas.setFont('Helvetica-Bold', 8.5)
        canvas.setFillColor(DARK)
        canvas.drawRightString(width - 18 * mm, height - 14 * mm, 'SISTEM MANAJEMEN PERTANIAN PADI')
        canvas.setFont('Helvetica', 7)
        canvas.setFillColor(MID)
        canvas.drawRightString(width - 18 * mm, height - 18.5 * mm, self.report_title)
        if self.season_label:
            canvas.drawRightString(width - 18 * mm, height - 23 * mm, self.season_label)

        # Footer
        canvas.setStrokeColor(BORDER)
        canvas.line(18 * mm, 15 * mm, width - 18 * mm, 15 * mm)
        canvas.setFont('Helvetica', 6.8)
        canvas.setFillColor(MID)
        canvas.drawString(18 * mm, 10.5 * mm, 'Padi Emas Nusantara • Menanam Harapan, Menuai Kesejahteraan')
        canvas.drawRightString(width - 18 * mm, 10.5 * mm, f'Halaman {doc.page}')
        canvas.restoreState()


def styles():
    s = getSampleStyleSheet()
    return {
        'title': ParagraphStyle('ptitle', parent=s['Title'], fontName='Helvetica-Bold', fontSize=17, leading=21, textColor=DARK, spaceAfter=3),
        'subtitle': ParagraphStyle('psub', parent=s['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=MID, spaceAfter=10),
        'section': ParagraphStyle('psection', parent=s['Heading2'], fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=DARK, spaceBefore=7, spaceAfter=7),
        'body': ParagraphStyle('pbody', parent=s['BodyText'], fontName='Helvetica', fontSize=7.8, leading=11, textColor=DARK),
        'small': ParagraphStyle('psmall', parent=s['BodyText'], fontName='Helvetica', fontSize=6.8, leading=9, textColor=MID),
        'kpi_label': ParagraphStyle('pkpilabel', parent=s['Normal'], fontName='Helvetica', fontSize=6.8, leading=8, textColor=MID),
        'kpi_value': ParagraphStyle('pkpivalue', parent=s['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=13, textColor=DARK),
        'th': ParagraphStyle('pth', parent=s['Normal'], fontName='Helvetica-Bold', fontSize=6.8, leading=8, textColor=colors.white),
        'td': ParagraphStyle('ptd', parent=s['Normal'], fontName='Helvetica', fontSize=6.8, leading=9, textColor=DARK),
        'td_right': ParagraphStyle('ptdr', parent=s['Normal'], fontName='Helvetica', fontSize=6.8, leading=9, textColor=DARK, alignment=TA_RIGHT),
        'td_bold': ParagraphStyle('ptdb', parent=s['Normal'], fontName='Helvetica-Bold', fontSize=6.8, leading=9, textColor=DARK),
        'note': ParagraphStyle('pnote', parent=s['Normal'], fontName='Helvetica', fontSize=7, leading=10, textColor=MID),
    }


def kpi_table(items, st):
    cells = []
    for label, value, note in items:
        cells.append([para(label, st['kpi_label']), para(value, st['kpi_value']), para(note, st['small'])])
    # Build each KPI as a compact nested table.
    nested = []
    for label, value, note in items:
        nested.append(Table([[para(label, st['kpi_label'])], [para(value, st['kpi_value'])], [para(note, st['small'])]], colWidths=[41.5 * mm], rowHeights=[5 * mm, 8 * mm, 5 * mm], style=TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0), ('TOPPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 0)
        ])))
    out = Table([nested], colWidths=[43.5 * mm] * 4, rowHeights=[25 * mm])
    out.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.6, BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.6, BORDER),
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    return out


def data_table(headers, rows, st, widths=None, right_cols=None):
    right_cols = set(right_cols or [])
    data = [[para(h, st['th']) for h in headers]]
    for row in rows:
        data.append([para(v, st['td_right'] if i in right_cols else st['td']) for i, v in enumerate(row)])
    if not widths:
        widths = [None] * len(headers)
    t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    commands = [
        ('BACKGROUND', (0, 0), (-1, 0), GREEN),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.35, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]
    for r in range(1, len(data)):
        if r % 2 == 0:
            commands.append(('BACKGROUND', (0, r), (-1, r), colors.HexColor('#f8fbf9')))
    t.setStyle(TableStyle(commands))
    return t


def report_title_block(title, subtitle, st):
    return [para(title, st['title']), para(subtitle, st['subtitle'])]


def get_scope(request):
    seasons = PlantingSeason.objects.all()
    sid = request.GET.get('season')
    season = seasons.filter(pk=sid).first() if sid else seasons.filter(status='AKTIF').first()
    return seasons, season


def build_pdf(request, report_type, season=None):
    st = styles()
    if season:
        season_label = season.name
    else:
        season_label = 'Seluruh musim tanam'
    report_names = {
        'financial': 'Laporan Keuangan',
        'gross': 'Laporan Peredaran Bruto',
        'balance': 'Neraca Keuangan',
        'tax': 'Laporan Pajak',
        'season': 'Laporan Musim Tanam',
    }
    title = report_names.get(report_type, 'Laporan Usaha')
    filename = f"padi-emas-{report_type}-{'musim-'+str(season.pk) if season else 'semua'}.pdf"

    buffer = BytesIO()
    doc = NumberedDocTemplate(buffer, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=37 * mm, bottomMargin=20 * mm,
                              title=title, author='Padi Emas Nusantara',
                              logo_path=str(settings.BASE_DIR / 'static' / 'img' / 'padi-emas-logo.png'),
                              report_title=title, season_label=season_label)
    story = []
    story += report_title_block(title, f"Dicetak {timezone.localdate().strftime('%d %B %Y')} • {season_label}", st)

    expenses = Expense.objects.filter(season=season) if season else Expense.objects.all()
    harvests = Harvest.objects.filter(season=season) if season else Harvest.objects.all()
    sales = Sale.objects.filter(season=season) if season else Sale.objects.all()
    expense_total = expenses.aggregate(v=Sum('amount'))['v'] or Decimal('0')
    harvest_total = harvests.aggregate(v=Sum('quantity_kg'))['v'] or Decimal('0')
    sales_total = sales.aggregate(v=Sum('total_amount'))['v'] or Decimal('0')
    sales_qty = sales.aggregate(v=Sum('quantity_kg'))['v'] or Decimal('0')
    profit = sales_total - expense_total
    stock_kg = max(harvest_total - sales_qty, Decimal('0'))

    if report_type == 'financial':
        story.append(kpi_table([
            ('Pendapatan Penjualan', money(sales_total), f'{sales.count()} transaksi'),
            ('Total Biaya', money(expense_total), f'{expenses.count()} transaksi'),
            ('Laba Bersih Sementara', money(profit), 'Penjualan − biaya'),
            ('Hasil Panen', f'{number(harvest_total)} Kg', f'Sisa {number(stock_kg)} Kg'),
        ], st))
        story.append(Spacer(1, 5 * mm))
        story.append(para('Analisis Profitabilitas', st['section']))
        cost_per_kg = expense_total / harvest_total if harvest_total else Decimal('0')
        sales_per_kg = sales_total / sales_qty if sales_qty else Decimal('0')
        rows = [
            ('Biaya per Kg panen', money(cost_per_kg)),
            ('Penjualan per Kg terjual', money(sales_per_kg)),
            ('Volume terjual', f'{number(sales_qty)} Kg'),
            ('Persediaan hasil panen', f'{number(stock_kg)} Kg'),
        ]
        story.append(data_table(['Indikator', 'Nilai'], rows, st, [110 * mm, 62 * mm], [1]))
        story.append(Spacer(1, 5 * mm))
        story.append(para('Rincian Biaya Operasional', st['section']))
        cats = expenses.values('category').annotate(total=Sum('amount')).order_by('-total')
        rows = [(r['category'], money(r['total'])) for r in cats]
        if not rows: rows = [('Belum ada pengeluaran', money(0))]
        story.append(data_table(['Kategori', 'Total'], rows, st, [110 * mm, 62 * mm], [1]))
        story.append(Spacer(1, 5 * mm))
        story.append(para(f"Kesimpulan: produksi tercatat {number(harvest_total)} Kg, penjualan {number(sales_qty)} Kg, dan estimasi stok {number(stock_kg)} Kg.", st['note']))

    elif report_type == 'gross':
        avg = sales_total / sales_qty if sales_qty else Decimal('0')
        story.append(kpi_table([
            ('Peredaran Bruto', money(sales_total), 'Total penjualan bruto'),
            ('Volume Penjualan', f'{number(sales_qty)} Kg', f'{sales.count()} transaksi'),
            ('Harga Rata-rata', f'{money(avg)}/Kg', 'Penjualan ÷ volume'),
            ('Periode', season.name if season else 'Semua Musim', 'Filter laporan'),
        ], st))
        story.append(Spacer(1, 5 * mm))
        story.append(para('Peredaran Bruto Bulanan', st['section']))
        monthly = sales.values('date__year', 'date__month').annotate(total=Sum('total_amount'), quantity=Sum('quantity_kg')).order_by('date__year', 'date__month')
        rows = [(f"{r['date__month']:02d}/{r['date__year']}", f"{number(r['quantity'])} Kg", money(r['total'])) for r in monthly]
        if not rows: rows = [('—', '0 Kg', money(0))]
        story.append(data_table(['Periode', 'Volume', 'Peredaran Bruto'], rows, st, [48 * mm, 50 * mm, 84 * mm], [1, 2]))
        story.append(Spacer(1, 5 * mm))
        story.append(para('Peredaran bruto merupakan total nilai penjualan yang tercatat sebelum pengurangan biaya operasional dan pajak.', st['note']))

    elif report_type == 'balance':
        if not season:
            season = PlantingSeason.objects.order_by('-start_date').first()
        if season:
            profile, _ = SeasonFinanceProfile.objects.get_or_create(season=season)
            expenses = Expense.objects.filter(season=season)
            harvests = Harvest.objects.filter(season=season)
            sales = Sale.objects.filter(season=season)
            expense_total = expenses.aggregate(v=Sum('amount'))['v'] or Decimal('0')
            sales_total = sales.aggregate(v=Sum('total_amount'))['v'] or Decimal('0')
            harvest_total = harvests.aggregate(v=Sum('quantity_kg'))['v'] or Decimal('0')
            sales_qty = sales.aggregate(v=Sum('quantity_kg'))['v'] or Decimal('0')
            cost_per_kg = expense_total / harvest_total if harvest_total else Decimal('0')
            stock_value = max(harvest_total - sales_qty, Decimal('0')) * cost_per_kg
            cash = profile.opening_cash + sales_total - expense_total
            total_assets = cash + stock_value + profile.fixed_assets + profile.other_assets
            equity = total_assets - profile.liabilities
            story.append(kpi_table([
                ('Total Aset', money(total_assets), 'Kas + stok + aset'),
                ('Kewajiban', money(profile.liabilities), 'Input per musim'),
                ('Ekuitas Bersih', money(equity), 'Aset − kewajiban'),
                ('Omzet Musim', money(sales_total), 'Total penjualan'),
            ], st))
            story.append(Spacer(1, 5 * mm))
            story.append(para('Posisi Aset', st['section']))
            rows = [
                ('Kas / Bank (estimasi)', money(cash)),
                ('Persediaan hasil panen', money(stock_value)),
                ('Aset tetap', money(profile.fixed_assets)),
                ('Aset lainnya', money(profile.other_assets)),
                ('Total Aset', money(total_assets)),
            ]
            story.append(data_table(['Pos', 'Nilai'], rows, st, [110 * mm, 62 * mm], [1]))
            story.append(Spacer(1, 5 * mm))
            story.append(para('Kewajiban & Ekuitas', st['section']))
            rows = [('Kewajiban', money(profile.liabilities)), ('Ekuitas bersih', money(equity)), ('Total Kewajiban + Ekuitas', money(total_assets))]
            story.append(data_table(['Pos', 'Nilai'], rows, st, [110 * mm, 62 * mm], [1]))
            story.append(Spacer(1, 5 * mm))
            story.append(para('Catatan: neraca ini adalah neraca manajerial sederhana. Kas dan persediaan dihitung secara estimasi dari transaksi yang tercatat.', st['note']))
        else:
            story.append(para('Belum ada musim tanam yang dapat dilaporkan.', st['body']))

    elif report_type == 'tax':
        profile = TaxProfile.objects.filter(is_active=True).first() or TaxProfile(rate=Decimal('0.500'), basis='OMZET')
        basis_amount = sales_total if profile.basis == 'OMZET' else max(profit, Decimal('0'))
        estimated_tax = (basis_amount * profile.rate / Decimal('100')).quantize(Decimal('0.01'))
        story.append(kpi_table([
            ('Omzet Penjualan', money(sales_total), 'Total transaksi penjualan'),
            ('Total Biaya', money(expense_total), 'Biaya operasional'),
            ('Dasar Pengenaan', money(basis_amount), profile.get_basis_display()),
            ('Estimasi Pajak', money(estimated_tax), f'Tarif {profile.rate}%'),
        ], st))
        story.append(Spacer(1, 5 * mm))
        story.append(para('Perhitungan Pajak', st['section']))
        rows = [('Dasar Pengenaan Pajak', money(basis_amount)), ('Tarif', f'{profile.rate}%'), ('Estimasi Pajak', money(estimated_tax))]
        story.append(data_table(['Komponen', 'Nilai'], rows, st, [110 * mm, 62 * mm], [1]))
        story.append(Spacer(1, 5 * mm))
        story.append(para(f'Catatan: {profile.note or "Laporan ini adalah estimasi internal, bukan penetapan pajak resmi."}', st['note']))

    elif report_type == 'season':
        if not season:
            season = PlantingSeason.objects.order_by('-start_date').first()
        if not season:
            story.append(para('Belum ada musim tanam.', st['body']))
        else:
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
            story.append(kpi_table([
                ('Total Pengeluaran', money(expense_total), f'{expenses.count()} transaksi'),
                ('Total Hasil Panen', f'{number(harvest_total)} Kg', f'{harvests.count()} catatan'),
                ('Total Penjualan', money(sales_total), f'{number(sales_qty)} Kg terjual'),
                ('Laba Bersih Sementara', money(profit), 'Penjualan − pengeluaran'),
            ], st))
            story.append(Spacer(1, 5 * mm))
            story.append(para('Identitas Musim Tanam', st['section']))
            period = season.start_date.strftime('%d %b %Y') + (f" – {season.end_date.strftime('%d %b %Y')}" if season.end_date else '')
            rows = [('Status', season.get_status_display()), ('Periode', period), ('Luas', f'{number(season.area_ha)} Ha'), ('Target Panen', f'{number(season.target_harvest_kg)} Kg'), ('Pencapaian Target', pct(min(progress, Decimal('100'))))]
            story.append(data_table(['Informasi', 'Nilai'], rows, st, [110 * mm, 62 * mm], [1]))
            story.append(Spacer(1, 5 * mm))
            story.append(para('Ringkasan Produksi & Keuangan', st['section']))
            rows = [('Hasil panen', f'{number(harvest_total)} Kg'), ('Penjualan', money(sales_total)), ('Volume terjual', f'{number(sales_qty)} Kg'), ('Sisa stok', f'{number(stock_kg)} Kg'), ('Pengeluaran', money(expense_total)), ('Laba', money(profit))]
            story.append(data_table(['Indikator', 'Nilai'], rows, st, [110 * mm, 62 * mm], [1]))
            story.append(Spacer(1, 5 * mm))
            story.append(para('Laporan ini menyatukan ringkasan operasional dan keuangan untuk satu musim tanam, sehingga dapat digunakan sebagai arsip evaluasi musim.', st['note']))

    doc.build(story)
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response


@finance_required
def report_pdf(request):
    report_type = request.GET.get('type', 'financial')
    seasons, season = get_scope(request)
    if report_type in {'balance', 'season'} and not season:
        season = seasons.order_by('-start_date').first()
    return build_pdf(request, report_type, season)
