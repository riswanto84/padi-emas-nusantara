from django.db import models


class PlantingSeason(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('AKTIF', 'Aktif'), ('SELESAI', 'Selesai')]
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    area_ha = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    target_harvest_kg = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.name


class LandingPage(models.Model):
    """Global company-profile content editable from Django Admin."""
    site_name = models.CharField(max_length=150, default='Padi Emas Nusantara')
    tagline = models.CharField(max_length=255, default='Menanam Harapan, Menuai Kesejahteraan')
    meta_description = models.CharField(max_length=320, default='Padi Emas Nusantara — company profile dan Sistem Manajemen Pertanian Padi.')
    logo = models.ImageField(upload_to='landing/logo/', blank=True, null=True)
    favicon = models.ImageField(upload_to='landing/favicon/', blank=True, null=True)

    hero_eyebrow = models.CharField(max_length=120, default='PADI EMAS NUSANTARA')
    hero_title = models.CharField(max_length=255, default='Menanam Harapan, Menuai Kesejahteraan')
    hero_text = models.TextField(default='Padi Emas Nusantara berkomitmen mendukung pertanian padi yang modern, efisien, dan berkelanjutan melalui teknologi, kolaborasi, dan pemberdayaan petani.')
    hero_image = models.ImageField(upload_to='landing/hero/', blank=True, null=True)
    hero_slogan = models.CharField(max_length=255, default='Pertanian Maju | Indonesia Kuat')

    about_eyebrow = models.CharField(max_length=100, default='TENTANG KAMI')
    about_title = models.CharField(max_length=200, default='Padi Emas Nusantara')
    about_text_1 = models.TextField(default='Padi Emas Nusantara adalah perusahaan yang bergerak di bidang pengelolaan pertanian padi secara terintegrasi, mulai dari perencanaan tanam, pengelolaan lahan, pendampingan petani, hingga pemasaran hasil panen.')
    about_text_2 = models.TextField(default='Kami menggabungkan pengalaman lapangan dengan teknologi digital untuk menciptakan pertanian yang lebih modern, efisien, dan berkelanjutan.')
    about_image = models.ImageField(upload_to='landing/about/', blank=True, null=True)
    about_quote = models.TextField(default='Bersama Petani, Mewujudkan Pertanian Indonesia yang Lebih Maju')
    stat_1_value = models.CharField(max_length=50, default='1.250+')
    stat_1_label = models.CharField(max_length=80, default='Petani Binaan')
    stat_2_value = models.CharField(max_length=50, default='5.000+')
    stat_2_label = models.CharField(max_length=80, default='Hektar Lahan')
    stat_3_value = models.CharField(max_length=50, default='28.500+')
    stat_3_label = models.CharField(max_length=80, default='Ton Hasil Panen')

    activities_eyebrow = models.CharField(max_length=100, default='KEGIATAN KAMI')
    activities_title = models.CharField(max_length=200, default='Dukung Seluruh Rantai Nilai Pertanian Padi')
    facilities_eyebrow = models.CharField(max_length=100, default='FASILITAS KAMI')
    facilities_title = models.CharField(max_length=200, default='Sarana Pendukung Pertanian Modern')
    gallery_eyebrow = models.CharField(max_length=100, default='GALERI KEGIATAN')
    gallery_title = models.CharField(max_length=200, default='Kegiatan Kami di Lapangan')
    gallery_button = models.CharField(max_length=100, default='Lihat Semua Galeri →')
    values_eyebrow = models.CharField(max_length=100, default='NILAI KAMI')
    values_title = models.CharField(max_length=200, default='Prinsip yang Selalu Kami Jaga')
    cta_eyebrow = models.CharField(max_length=120, default='BERSAMA PADI EMAS NUSANTARA')
    cta_title = models.CharField(max_length=255, default='Wujudkan Pertanian Indonesia yang Lebih Maju')
    cta_text = models.TextField(default='Bergabung bersama kami dalam membangun masa depan pertanian yang lebih baik.')

    system_eyebrow = models.CharField(max_length=100, default='TEKNOLOGI DIGITAL')
    system_title = models.CharField(max_length=200, default='Sistem Manajemen Pertanian Padi')
    system_text = models.TextField(default='Kelola data tanam, kegiatan, hasil panen, penjualan, keuangan, dan analisis usaha secara digital dalam satu sistem.')

    contact_address = models.TextField(default='Muara Gembong, Kabupaten Bekasi, Jawa Barat, Indonesia')
    contact_phone = models.CharField(max_length=80, default='+62 812 3456 7890')
    contact_email = models.EmailField(default='info@padiemasnusantara.id')
    instagram_url = models.URLField(blank=True, default='')
    youtube_url = models.URLField(blank=True, default='')
    facebook_url = models.URLField(blank=True, default='')
    linkedin_url = models.URLField(blank=True, default='')
    footer_text = models.CharField(max_length=255, default='Menanam Harapan, Menuai Kesejahteraan')
    copyright_text = models.CharField(max_length=255, default='© 2026 Padi Emas Nusantara')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Konten Landing Page'
        verbose_name_plural = 'Konten Landing Page'

    def __str__(self):
        return self.site_name

    @classmethod
    def get_solo(cls):
        obj = cls.objects.first()
        if not obj:
            obj = cls.objects.create()
        return obj


class LandingFeature(models.Model):
    icon = models.CharField(max_length=20, default='🌱')
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Highlight Hero'
        verbose_name_plural = 'Highlight Hero'

    def __str__(self):
        return self.title


class LandingActivity(models.Model):
    icon = models.CharField(max_length=20, default='🌱')
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Kegiatan'
        verbose_name_plural = 'Kegiatan'

    def __str__(self):
        return self.title


class LandingFacility(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='landing/facilities/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Fasilitas'
        verbose_name_plural = 'Fasilitas'

    def __str__(self):
        return self.title


class LandingGallery(models.Model):
    title = models.CharField(max_length=120, blank=True)
    image = models.ImageField(upload_to='landing/gallery/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Galeri'
        verbose_name_plural = 'Galeri'

    def __str__(self):
        return self.title or f'Galeri #{self.pk or "baru"}'


class LandingValue(models.Model):
    icon = models.CharField(max_length=20, default='✦')
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Nilai Perusahaan'
        verbose_name_plural = 'Nilai Perusahaan'

    def __str__(self):
        return self.title
