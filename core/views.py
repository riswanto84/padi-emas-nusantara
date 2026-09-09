from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.utils import timezone

import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from finance.models import Expense
from harvest.models import Harvest
from sales.models import Sale
from .models import PlantingSeason, LandingPage, LandingFeature, LandingActivity, LandingFacility, LandingGallery, LandingValue


def is_admin(user):
    return user.is_authenticated and user.is_superuser


def staff_required(view):
    return user_passes_test(lambda u: u.is_staff)(view)


MUARA_GEMBONG_LAT = -6.0056793513
MUARA_GEMBONG_LON = 107.0905934740


def weather_forecast(request):
    """Return live weather forecast for Muara Gembong from Open-Meteo."""
    params = {
        'latitude': MUARA_GEMBONG_LAT,
        'longitude': MUARA_GEMBONG_LON,
        'current': 'temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m',
        'daily': 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,wind_speed_10m_max,sunrise,sunset',
        'timezone': 'Asia/Jakarta',
        'forecast_days': 5,
    }
    url = 'https://api.open-meteo.com/v1/forecast?' + urlencode(params)
    try:
        req = Request(url, headers={'Accept': 'application/json', 'User-Agent': 'PadiEmasNusantara/1.0'})
        with urlopen(req, timeout=8) as response:
            payload = json.loads(response.read().decode('utf-8'))
        payload['source'] = 'Open-Meteo'
        payload['location_name'] = 'Muara Gembong, Kabupaten Bekasi'
        return JsonResponse(payload)
    except Exception as exc:
        return JsonResponse({
            'error': 'Data cuaca Open-Meteo tidak dapat diambil saat ini.',
            'detail': str(exc),
        }, status=503)


def landing_page(request):
    """Public company-profile landing page, fully editable from Django Admin."""
    context = {
        'landing': LandingPage.get_solo(),
        'landing_features': LandingFeature.objects.filter(is_active=True),
        'landing_activities': LandingActivity.objects.filter(is_active=True),
        'landing_facilities': LandingFacility.objects.filter(is_active=True),
        'landing_gallery': LandingGallery.objects.filter(is_active=True),
        'landing_values': LandingValue.objects.filter(is_active=True),
    }
    return render(request, 'landing.html', context)


@login_required
def dashboard(request):
    season_id = request.GET.get('season')
    season = PlantingSeason.objects.filter(pk=season_id).first() if season_id else PlantingSeason.objects.filter(status='AKTIF').first()
    base_e = Expense.objects.filter(season=season) if season else Expense.objects.all()
    base_h = Harvest.objects.filter(season=season) if season else Harvest.objects.all()
    base_s = Sale.objects.filter(season=season) if season else Sale.objects.all()
    e = base_e.aggregate(v=Sum('amount'))['v'] or 0
    h = base_h.aggregate(v=Sum('quantity_kg'))['v'] or 0
    s = base_s.aggregate(v=Sum('total_amount'))['v'] or 0

    # DOC (Day of Culture/umur tanaman) dihitung dari tanggal mulai musim.
    # Untuk musim selesai, DOC berhenti pada tanggal selesai; untuk musim aktif,
    # DOC berjalan sampai hari ini. Perhitungan inklusif: hari mulai = DOC 1.
    doc = None
    doc_label = 'Belum dimulai'
    if season:
        doc_end = season.end_date if season.status == 'SELESAI' and season.end_date else timezone.localdate()
        if season.start_date:
            if doc_end >= season.start_date:
                doc = (doc_end - season.start_date).days + 1
                doc_label = f'DOC {doc}'
            else:
                doc_label = 'Belum dimulai'

    context = {
        'season': season,
        'total_expenses': e,
        'total_harvest': h,
        'total_sales': s,
        'profit': s - e,
        'season_count': PlantingSeason.objects.count(),
        'season_doc': doc,
        'season_doc_label': doc_label,
    }
    return render(request, 'dashboard.html', context)


@login_required
@staff_required
def season_list(request):
    return render(request, 'core/season_list.html', {'seasons': PlantingSeason.objects.all()})


@login_required
@staff_required
def season_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        start = request.POST.get('start_date')
        area = request.POST.get('area_ha') or 0
        target = request.POST.get('target_harvest_kg') or 0
        if PlantingSeason.objects.filter(status='AKTIF').exists():
            messages.error(request, 'Tutup musim tanam aktif sebelum memulai musim baru.')
        elif not name or not start:
            messages.error(request, 'Nama musim tanam dan tanggal mulai wajib diisi.')
        elif PlantingSeason.objects.filter(name=name).exists():
            messages.error(request, 'Nama musim tanam sudah digunakan.')
        else:
            PlantingSeason.objects.create(
                name=name,
                start_date=start,
                area_ha=area,
                target_harvest_kg=target,
                notes=request.POST.get('notes', ''),
                status='AKTIF',
            )
            messages.success(request, 'Musim tanam berhasil dimulai.')
            return redirect('season_list')
    return render(request, 'core/season_form.html')


@login_required
@staff_required
def season_close(request, pk):
    season = get_object_or_404(PlantingSeason, pk=pk)
    if request.method == 'POST':
        season.status = 'SELESAI'
        season.end_date = timezone.localdate()
        season.save(update_fields=['status', 'end_date'])
        messages.success(request, f'{season.name} berhasil ditutup.')
    return redirect('season_list')


@login_required
@user_passes_test(is_admin)
def user_list(request):
    User = get_user_model()
    users = User.objects.prefetch_related('groups').order_by('username')
    return render(request, 'core/user_list.html', {'users': users, 'groups': Group.objects.order_by('name')})


@login_required
@user_passes_test(is_admin)
def user_create(request):
    User = get_user_model()
    groups = Group.objects.order_by('name')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        selected_roles = request.POST.getlist('roles')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan.')
        elif not password:
            messages.error(request, 'Password wajib diisi.')
        elif not selected_roles:
            messages.error(request, 'Pilih minimal satu role.')
        else:
            u = User.objects.create_user(
                username=username,
                password=password,
                email=request.POST.get('email', '').strip(),
                first_name=request.POST.get('first_name', '').strip(),
                last_name=request.POST.get('last_name', '').strip(),
            )
            selected_groups = list(groups.filter(name__in=selected_roles))
            u.groups.set(selected_groups)
            u.is_staff = 'Administrator' in selected_roles
            u.is_superuser = 'Administrator' in selected_roles
            u.save(update_fields=['is_staff', 'is_superuser'])
            messages.success(request, f'User {username} berhasil dibuat dengan {len(selected_groups)} role.')
            return redirect('user_list')
    return render(request, 'core/user_form.html', {'groups': groups, 'selected_roles': []})


@login_required
@user_passes_test(is_admin)
def user_edit(request, pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=pk)
    groups = Group.objects.order_by('name')
    if request.method == 'POST':
        selected_roles = request.POST.getlist('roles')
        if not selected_roles:
            messages.error(request, 'Pilih minimal satu role.')
        else:
            # Jangan sampai administrator mencabut hak administrator dari akun yang sedang dipakai.
            if user.pk == request.user.pk and 'Administrator' not in selected_roles:
                selected_roles.append('Administrator')
                messages.info(request, 'Role Administrator dipertahankan karena Anda sedang mengubah akun yang sedang digunakan.')
            user.first_name = request.POST.get('first_name', '').strip()
            user.last_name = request.POST.get('last_name', '').strip()
            user.email = request.POST.get('email', '').strip()
            user.groups.set(groups.filter(name__in=selected_roles))
            user.is_staff = 'Administrator' in selected_roles
            user.is_superuser = 'Administrator' in selected_roles
            if request.POST.get('password'):
                user.set_password(request.POST['password'])
            user.save()
            messages.success(request, f'User {user.username} berhasil diperbarui.')
            return redirect('user_list')
    selected_roles = list(user.groups.values_list('name', flat=True))
    if user.is_superuser and 'Administrator' not in selected_roles:
        selected_roles.append('Administrator')
    return render(request, 'core/user_form.html', {'groups': groups, 'user_obj': user, 'selected_roles': selected_roles, 'is_edit': True})
