from django.db import migrations, models
import django.db.models.deletion


def seed_landing(apps, schema_editor):
    LandingPage = apps.get_model('core', 'LandingPage')
    LandingFeature = apps.get_model('core', 'LandingFeature')
    LandingActivity = apps.get_model('core', 'LandingActivity')
    LandingFacility = apps.get_model('core', 'LandingFacility')
    LandingValue = apps.get_model('core', 'LandingValue')
    LandingPage.objects.get_or_create(pk=1)
    features = [
        ('🌱', 'Pertanian Berkelanjutan', 'Untuk generasi mendatang'),
        ('👥', 'Kolaborasi Petani', 'Bersama membangun masa depan'),
        ('▥', 'Berbasis Data', 'Keputusan lebih tepat dan terukur'),
        ('✓', 'Aman & Terpercaya', 'Komitmen pada integritas'),
    ]
    activities = [
        ('▣', 'Perencanaan Tanam', 'Pemilihan varietas, penjadwalan, dan pengolahan lahan.'),
        ('♧', 'Pendampingan Petani', 'Pelatihan, konsultasi, dan praktik lapangan.'),
        ('🌱', 'Pengelolaan Lahan', 'Teknologi dan manajemen lahan yang efisien.'),
        ('◉', 'Panen & Pascapanen', 'Dukungan alat dan sarana pascapanen.'),
        ('⌁', 'Pemasaran', 'Akses pasar yang lebih luas dan berkelanjutan.'),
        ('▥', 'Analisis Usaha Tani', 'Data dan laporan untuk keputusan yang lebih baik.'),
    ]
    facilities = [
        ('Alat & Mesin Pertanian', 'Traktor, combine harvester, dan peralatan pendukung.'),
        ('Gudang & Penyimpanan', 'Sistem penyimpanan hasil panen yang terstandar.'),
        ('Sistem Irigasi', 'Pengelolaan air yang efisien dan berkelanjutan.'),
        ('Teknologi Digital', 'Pemantauan lahan dengan data dan teknologi.'),
    ]
    values = [
        ('◈', 'Integritas', 'Jujur, transparan, dan profesional.'),
        ('✦', 'Inovasi', 'Terus belajar dan mengadopsi teknologi.'),
        ('♧', 'Kemitraan', 'Tumbuh bersama petani dan seluruh mitra.'),
        ('🌿', 'Keberlanjutan', 'Menjaga lingkungan untuk generasi mendatang.'),
    ]
    for i, (icon, title, description) in enumerate(features):
        LandingFeature.objects.get_or_create(title=title, defaults={'icon': icon, 'description': description, 'order': i})
    for i, (icon, title, description) in enumerate(activities):
        LandingActivity.objects.get_or_create(title=title, defaults={'icon': icon, 'description': description, 'order': i})
    for i, (title, description) in enumerate(facilities):
        LandingFacility.objects.get_or_create(title=title, defaults={'description': description, 'order': i})
    for i, (icon, title, description) in enumerate(values):
        LandingValue.objects.get_or_create(title=title, defaults={'icon': icon, 'description': description, 'order': i})


class Migration(migrations.Migration):
    dependencies = [('core', '0001_initial')]

    operations = [
        migrations.CreateModel(
            name='LandingPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='Padi Emas Nusantara', max_length=150)),
                ('tagline', models.CharField(default='Menanam Harapan, Menuai Kesejahteraan', max_length=255)),
                ('meta_description', models.CharField(default='Padi Emas Nusantara — company profile dan Sistem Manajemen Pertanian Padi.', max_length=320)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='landing/logo/')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='landing/favicon/')),
                ('hero_eyebrow', models.CharField(default='PADI EMAS NUSANTARA', max_length=120)),
                ('hero_title', models.CharField(default='Menanam Harapan, Menuai Kesejahteraan', max_length=255)),
                ('hero_text', models.TextField(default='Padi Emas Nusantara berkomitmen mendukung pertanian padi yang modern, efisien, dan berkelanjutan melalui teknologi, kolaborasi, dan pemberdayaan petani.')),
                ('hero_image', models.ImageField(blank=True, null=True, upload_to='landing/hero/')),
                ('hero_slogan', models.CharField(default='Pertanian Maju | Indonesia Kuat', max_length=255)),
                ('about_eyebrow', models.CharField(default='TENTANG KAMI', max_length=100)),
                ('about_title', models.CharField(default='Padi Emas Nusantara', max_length=200)),
                ('about_text_1', models.TextField(default='Padi Emas Nusantara adalah perusahaan yang bergerak di bidang pengelolaan pertanian padi secara terintegrasi, mulai dari perencanaan tanam, pengelolaan lahan, pendampingan petani, hingga pemasaran hasil panen.')),
                ('about_text_2', models.TextField(default='Kami menggabungkan pengalaman lapangan dengan teknologi digital untuk menciptakan pertanian yang lebih modern, efisien, dan berkelanjutan.')),
                ('about_image', models.ImageField(blank=True, null=True, upload_to='landing/about/')),
                ('about_quote', models.TextField(default='Bersama Petani, Mewujudkan Pertanian Indonesia yang Lebih Maju')),
                ('stat_1_value', models.CharField(default='1.250+', max_length=50)),
                ('stat_1_label', models.CharField(default='Petani Binaan', max_length=80)),
                ('stat_2_value', models.CharField(default='5.000+', max_length=50)),
                ('stat_2_label', models.CharField(default='Hektar Lahan', max_length=80)),
                ('stat_3_value', models.CharField(default='28.500+', max_length=50)),
                ('stat_3_label', models.CharField(default='Ton Hasil Panen', max_length=80)),
                ('activities_eyebrow', models.CharField(default='KEGIATAN KAMI', max_length=100)),
                ('activities_title', models.CharField(default='Dukung Seluruh Rantai Nilai Pertanian Padi', max_length=200)),
                ('facilities_eyebrow', models.CharField(default='FASILITAS KAMI', max_length=100)),
                ('facilities_title', models.CharField(default='Sarana Pendukung Pertanian Modern', max_length=200)),
                ('gallery_eyebrow', models.CharField(default='GALERI KEGIATAN', max_length=100)),
                ('gallery_title', models.CharField(default='Kegiatan Kami di Lapangan', max_length=200)),
                ('gallery_button', models.CharField(default='Lihat Semua Galeri →', max_length=100)),
                ('values_eyebrow', models.CharField(default='NILAI KAMI', max_length=100)),
                ('values_title', models.CharField(default='Prinsip yang Selalu Kami Jaga', max_length=200)),
                ('cta_eyebrow', models.CharField(default='BERSAMA PADI EMAS NUSANTARA', max_length=120)),
                ('cta_title', models.CharField(default='Wujudkan Pertanian Indonesia yang Lebih Maju', max_length=255)),
                ('cta_text', models.TextField(default='Bergabung bersama kami dalam membangun masa depan pertanian yang lebih baik.')),
                ('system_eyebrow', models.CharField(default='TEKNOLOGI DIGITAL', max_length=100)),
                ('system_title', models.CharField(default='Sistem Manajemen Pertanian Padi', max_length=200)),
                ('system_text', models.TextField(default='Kelola data tanam, kegiatan, hasil panen, penjualan, keuangan, dan analisis usaha secara digital dalam satu sistem.')),
                ('contact_address', models.TextField(default='Muara Gembong, Kabupaten Bekasi, Jawa Barat, Indonesia')),
                ('contact_phone', models.CharField(default='+62 812 3456 7890', max_length=80)),
                ('contact_email', models.EmailField(default='info@padiemasnusantara.id', max_length=254)),
                ('instagram_url', models.URLField(blank=True, default='')),
                ('youtube_url', models.URLField(blank=True, default='')),
                ('facebook_url', models.URLField(blank=True, default='')),
                ('linkedin_url', models.URLField(blank=True, default='')),
                ('footer_text', models.CharField(default='Menanam Harapan, Menuai Kesejahteraan', max_length=255)),
                ('copyright_text', models.CharField(default='© 2026 Padi Emas Nusantara', max_length=255)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'verbose_name': 'Konten Landing Page', 'verbose_name_plural': 'Konten Landing Page'},
        ),
        migrations.CreateModel(
            name='LandingFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(default='🌱', max_length=20)),
                ('title', models.CharField(max_length=120)),
                ('description', models.CharField(max_length=255)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'verbose_name': 'Highlight Hero', 'verbose_name_plural': 'Highlight Hero', 'ordering': ['order', 'id']},
        ),
        migrations.CreateModel(
            name='LandingActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(default='🌱', max_length=20)),
                ('title', models.CharField(max_length=120)),
                ('description', models.CharField(max_length=255)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'verbose_name': 'Kegiatan', 'verbose_name_plural': 'Kegiatan', 'ordering': ['order', 'id']},
        ),
        migrations.CreateModel(
            name='LandingFacility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='landing/facilities/')),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'verbose_name': 'Fasilitas', 'verbose_name_plural': 'Fasilitas', 'ordering': ['order', 'id']},
        ),
        migrations.CreateModel(
            name='LandingGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=120)),
                ('image', models.ImageField(upload_to='landing/gallery/')),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'verbose_name': 'Galeri', 'verbose_name_plural': 'Galeri', 'ordering': ['order', 'id']},
        ),
        migrations.CreateModel(
            name='LandingValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(default='✦', max_length=20)),
                ('title', models.CharField(max_length=120)),
                ('description', models.CharField(max_length=255)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'verbose_name': 'Nilai Perusahaan', 'verbose_name_plural': 'Nilai Perusahaan', 'ordering': ['order', 'id']},
        ),
        migrations.RunPython(
            code=seed_landing,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
