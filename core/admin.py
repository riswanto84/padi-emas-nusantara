from django.contrib import admin
from django.utils.html import format_html

from .models import (
    PlantingSeason,
    LandingPage,
    LandingFeature,
    LandingActivity,
    LandingFacility,
    LandingGallery,
    LandingValue,
)


class OrderedActiveAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'id')
    search_fields = ('title', 'description')


@admin.register(PlantingSeason)
class PlantingSeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'area_ha', 'target_harvest_kg', 'status')
    list_filter = ('status',)
    search_fields = ('name',)


@admin.register(LandingPage)
class LandingPageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identitas & SEO', {'fields': ('site_name', 'tagline', 'meta_description', 'logo', 'favicon')}),
        ('Hero / Beranda', {'fields': ('hero_eyebrow', 'hero_title', 'hero_text', 'hero_image', 'hero_slogan')}),
        ('Tentang Kami', {'fields': ('about_eyebrow', 'about_title', 'about_text_1', 'about_text_2', 'about_image', 'about_quote')}),
        ('Statistik', {'fields': (
            ('stat_1_value', 'stat_1_label'),
            ('stat_2_value', 'stat_2_label'),
            ('stat_3_value', 'stat_3_label'),
        )}),
        ('Bagian Kegiatan & Keunggulan', {'fields': ('activities_eyebrow', 'activities_title', 'facilities_eyebrow', 'facilities_title', 'gallery_eyebrow', 'gallery_title', 'gallery_button', 'values_eyebrow', 'values_title')}),
        ('Call To Action', {'fields': ('cta_eyebrow', 'cta_title', 'cta_text')}),
        ('Sistem Manajemen Pertanian', {'fields': ('system_eyebrow', 'system_title', 'system_text')}),
        ('Kontak & Footer', {'fields': (
            'contact_address', 'contact_phone', 'contact_email',
            'instagram_url', 'youtube_url', 'facebook_url', 'linkedin_url',
            'footer_text', 'copyright_text',
        )}),
    )

    def has_add_permission(self, request):
        return not LandingPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(LandingFeature)
class LandingFeatureAdmin(OrderedActiveAdmin):
    pass


@admin.register(LandingActivity)
class LandingActivityAdmin(OrderedActiveAdmin):
    pass


@admin.register(LandingFacility)
class LandingFacilityAdmin(OrderedActiveAdmin):
    list_display = ('title', 'image_preview', 'order', 'is_active')

    @admin.display(description='Gambar')
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:90px;height:55px;object-fit:cover;border-radius:8px;" />', obj.image.url)
        return '—'


@admin.register(LandingGallery)
class LandingGalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'id')
    search_fields = ('title',)

    @admin.display(description='Gambar')
    def image_preview(self, obj):
        return format_html('<img src="{}" style="width:100px;height:65px;object-fit:cover;border-radius:8px;" />', obj.image.url) if obj.image else '—'


@admin.register(LandingValue)
class LandingValueAdmin(OrderedActiveAdmin):
    pass


admin.site.site_header = 'Padi Emas Nusantara — Administrasi'
admin.site.site_title = 'Padi Emas Nusantara'
admin.site.index_title = 'Kelola Website & Sistem Manajemen Pertanian'
