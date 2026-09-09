from django.db import models
from core.models import PlantingSeason
class Expense(models.Model):
    season = models.ForeignKey(PlantingSeason, on_delete=models.PROTECT, related_name="finance_expenses", null=True, blank=True)
    date=models.DateField()
    category=models.CharField(max_length=80)
    description=models.CharField(max_length=255)
    amount=models.DecimalField(max_digits=14,decimal_places=2)
    class Meta: ordering=['-date']
    def __str__(self): return self.description


class TaxProfile(models.Model):
    BASIS_CHOICES = [
        ('OMZET', 'Persentase omzet penjualan'),
        ('LABA', 'Persentase laba setelah biaya'),
    ]
    name = models.CharField(max_length=100, default='Pajak Usaha')
    rate = models.DecimalField(max_digits=6, decimal_places=3, default=0.500)
    basis = models.CharField(max_length=10, choices=BASIS_CHOICES, default='OMZET')
    is_active = models.BooleanField(default=True)
    note = models.CharField(max_length=255, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_active', 'name']

    def __str__(self):
        return self.name


class SeasonFinanceProfile(models.Model):
    season = models.OneToOneField(PlantingSeason, on_delete=models.CASCADE, related_name='finance_profile')
    opening_cash = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    fixed_assets = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    other_assets = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    liabilities = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    note = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profil Keuangan Musim Tanam'
        verbose_name_plural = 'Profil Keuangan Musim Tanam'

    def __str__(self):
        return f'Profil Keuangan - {self.season.name}'
