from decimal import Decimal
from datetime import date, timedelta
import random

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from core.models import PlantingSeason
from finance.models import Expense, TaxProfile, SeasonFinanceProfile
from harvest.models import Harvest
from sales.models import Sale


class Command(BaseCommand):
    help = 'Membuat data dummy Padi Emas Nusantara: 3 musim dan total 1.000 transaksi.'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Hapus transaksi dan musim dummy sebelum membuat ulang.')
        parser.add_argument('--count', type=int, default=1000, help='Jumlah total transaksi dummy (default: 1000).')

    @transaction.atomic
    def handle(self, *args, **opts):
        if opts['count'] < 3:
            raise ValueError('--count minimal 3.')

        User = get_user_model()
        rng = random.Random(20260909)

        roles = ['Administrator', 'Manajer', 'Keuangan', 'Operator Lapangan']
        for name in roles:
            Group.objects.get_or_create(name=name)

        all_models = [PlantingSeason, Expense, Harvest, Sale]
        Group.objects.get(name='Administrator').permissions.set(Permission.objects.all())
        Group.objects.get(name='Manajer').permissions.set(self.perms_for(all_models))
        Group.objects.get(name='Keuangan').permissions.set(self.perms_for([Expense, Sale, Harvest]))
        Group.objects.get(name='Operator Lapangan').permissions.set(self.perms_for([Harvest, Expense]))

        if opts['clear']:
            Sale.objects.all().delete()
            Harvest.objects.all().delete()
            Expense.objects.all().delete()
            SeasonFinanceProfile.objects.all().delete()
            PlantingSeason.objects.all().delete()
            self.stdout.write(self.style.WARNING('Data transaksi, profil keuangan, dan musim tanam dihapus.'))

        TaxProfile.objects.update_or_create(
            name='PPh Final/Omzet',
            defaults={
                'rate': Decimal('0.500'),
                'basis': 'OMZET',
                'is_active': True,
                'note': 'Tarif dummy untuk demonstrasi; sesuaikan dengan status perpajakan usaha.',
            },
        )

        season_specs = [
            {
                'name': 'MT 2024/2025', 'start': date(2024, 9, 1), 'end': date(2025, 2, 10),
                'area': '18.50', 'target': '32000', 'status': 'SELESAI',
                'cash': '35000000', 'fixed': '60000000', 'other': '7000000', 'liab': '12000000',
            },
            {
                'name': 'MT 2025/2026', 'start': date(2025, 9, 5), 'end': date(2026, 2, 5),
                'area': '20.00', 'target': '36000', 'status': 'SELESAI',
                'cash': '45000000', 'fixed': '70000000', 'other': '9000000', 'liab': '15000000',
            },
            {
                'name': 'MT 2026/2027', 'start': date(2026, 9, 1), 'end': None,
                'area': '25.00', 'target': '45000', 'status': 'AKTIF',
                'cash': '50000000', 'fixed': '75000000', 'other': '10000000', 'liab': '25000000',
            },
        ]

        seasons = []
        for spec in season_specs:
            season, _ = PlantingSeason.objects.get_or_create(
                name=spec['name'],
                defaults={
                    'start_date': spec['start'],
                    'end_date': spec['end'],
                    'area_ha': Decimal(spec['area']),
                    'target_harvest_kg': Decimal(spec['target']),
                    'status': spec['status'],
                    'notes': 'Data dummy untuk demonstrasi dan pengujian laporan per musim tanam.',
                },
            )
            # Pastikan seed lama yang sudah ada tetap memiliki metadata musim yang benar.
            season.start_date = spec['start']
            season.end_date = spec['end']
            season.area_ha = Decimal(spec['area'])
            season.target_harvest_kg = Decimal(spec['target'])
            season.status = spec['status']
            season.notes = 'Data dummy untuk demonstrasi dan pengujian laporan per musim tanam.'
            season.save()
            SeasonFinanceProfile.objects.update_or_create(
                season=season,
                defaults={
                    'opening_cash': Decimal(spec['cash']),
                    'fixed_assets': Decimal(spec['fixed']),
                    'other_assets': Decimal(spec['other']),
                    'liabilities': Decimal(spec['liab']),
                    'note': 'Data awal dummy untuk contoh neraca dan laporan keuangan musim tanam.',
                },
            )
            seasons.append(season)

        # Distribusi tepat 1.000 transaksi: 400 pengeluaran + 300 panen + 300 penjualan.
        expense_count = opts['count'] * 40 // 100
        harvest_count = opts['count'] * 30 // 100
        sale_count = opts['count'] - expense_count - harvest_count

        # Saat seed dijalankan ulang tanpa --clear, hapus hanya data transaksi seed yang ada
        # agar jumlah data tetap tepat dan tidak menggandakan transaksi.
        Sale.objects.filter(season__in=seasons).delete()
        Harvest.objects.filter(season__in=seasons).delete()
        Expense.objects.filter(season__in=seasons).delete()

        expense_categories = [
            ('Pengolahan Tanah', (1200000, 9000000)),
            ('Benih', (800000, 6500000)),
            ('Pupuk', (1000000, 8500000)),
            ('Pestisida', (500000, 5000000)),
            ('Tenaga Kerja', (750000, 7000000)),
            ('Irigasi', (500000, 4000000)),
            ('Panen', (1500000, 8500000)),
            ('Transportasi', (500000, 4500000)),
            ('Sewa Alat', (1000000, 6000000)),
            ('Lain-lain', (250000, 2500000)),
        ]
        expense_rows = []
        for i in range(expense_count):
            season = seasons[i % 3]
            spec = season_specs[i % 3]
            cat, (low, high) = expense_categories[i % len(expense_categories)]
            start = spec['start']
            max_days = 165 if season.status == 'SELESAI' else max(1, (date(2027, 2, 28) - start).days)
            d = start + timedelta(days=rng.randint(0, max_days))
            amount = Decimal(rng.randrange(low // 50000, high // 50000 + 1) * 50000)
            expense_rows.append(Expense(
                season=season,
                date=d,
                category=cat,
                description=f'{cat} kegiatan lapangan #{i + 1:04d}',
                amount=amount,
            ))
        Expense.objects.bulk_create(expense_rows, batch_size=500)

        harvest_rows = []
        harvest_descriptions = ['Panen Petak A', 'Panen Petak B', 'Panen Petak C', 'Panen Petak D', 'Panen Petak E', 'Panen Petak F']
        for i in range(harvest_count):
            season = seasons[i % 3]
            spec = season_specs[i % 3]
            # Musim aktif menggunakan tanggal sampai akhir Februari 2027 untuk data demo.
            max_days = 165 if season.status == 'SELESAI' else max(1, (date(2027, 2, 28) - spec['start']).days)
            d = spec['start'] + timedelta(days=rng.randint(max(1, max_days - 25), max_days))
            qty = Decimal(rng.randrange(350, 1201) * 10)  # 3.500 - 12.000 kg
            moisture = Decimal(str(round(rng.uniform(20.0, 28.0), 2)))
            harvest_rows.append(Harvest(
                season=season,
                date=d,
                description=f'{harvest_descriptions[i % len(harvest_descriptions)]} #{i + 1:04d}',
                quantity_kg=qty,
                moisture=moisture,
            ))
        Harvest.objects.bulk_create(harvest_rows, batch_size=500)

        sale_rows = []
        customers = ['UD Beras Makmur', 'CV Tani Sejahtera', 'Penggilingan Jaya', 'Koperasi Pangan', 'PT Nusantara Pangan', 'Toko Berkah', 'Mitra Pangan', 'Distributor Gabah Nusantara']
        products = ['Gabah', 'Beras']
        statuses = ['LUNAS', 'LUNAS', 'LUNAS', 'SEBAGIAN', 'BELUM']
        for i in range(sale_count):
            season = seasons[i % 3]
            spec = season_specs[i % 3]
            max_days = 165 if season.status == 'SELESAI' else max(1, (date(2027, 2, 28) - spec['start']).days)
            d = spec['start'] + timedelta(days=rng.randint(max(1, max_days - 20), max_days))
            qty = Decimal(rng.randrange(200, 1601) * 5)  # 1.000 - 8.000 kg
            price = Decimal(rng.randrange(5800, 8201) * 50)  # Rp290.000 - Rp410.000/50kg equivalent
            total = qty * price
            sale_rows.append(Sale(
                season=season,
                date=d,
                customer=customers[i % len(customers)],
                product=products[i % len(products)],
                quantity_kg=qty,
                price_per_kg=price,
                total_amount=total,
                status=statuses[i % len(statuses)],
            ))
        Sale.objects.bulk_create(sale_rows, batch_size=500)

        users = [
            ('admin', 'admin12345', ['Administrator'], True, True),
            ('manager', 'manager12345', ['Manajer'], True, False),
            ('keuangan', 'keuangan12345', ['Keuangan'], True, False),
            ('supervisor', 'supervisor12345', ['Manajer', 'Keuangan'], True, False),
            ('operator', 'operator12345', ['Operator Lapangan'], False, False),
        ]
        for username, pwd, user_roles, staff, superuser in users:
            u, _ = User.objects.get_or_create(
                username=username,
                defaults={'email': f'{username}@padiemas.local'},
            )
            u.email = f'{username}@padiemas.local'
            u.is_staff = staff
            u.is_superuser = superuser
            u.set_password(pwd)
            u.save()
            u.groups.set([Group.objects.get(name=r) for r in user_roles])

        self.stdout.write(self.style.SUCCESS('Seed dummy berhasil.'))
        self.stdout.write(f'3 musim tanam: {", ".join(s.name for s in seasons)}')
        self.stdout.write(f'Total transaksi: {expense_count + harvest_count + sale_count:,}'.replace(',', '.'))
        self.stdout.write(f'Pengeluaran: {expense_count:,}'.replace(',', '.') + ' | Panen: ' + f'{harvest_count:,}'.replace(',', '.') + ' | Penjualan: ' + f'{sale_count:,}'.replace(',', '.'))
        self.stdout.write('Users: admin/admin12345 | manager/manager12345 | keuangan/keuangan12345 | supervisor/supervisor12345 | operator/operator12345')

    def perms_for(self, models):
        out = []
        for model in models:
            ct = ContentType.objects.get_for_model(model)
            out.extend(Permission.objects.filter(content_type=ct))
        return out
