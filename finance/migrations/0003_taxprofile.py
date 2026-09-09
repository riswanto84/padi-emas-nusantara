from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('finance', '0002_expense_season')]
    operations = [migrations.CreateModel(
        name='TaxProfile',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(default='Pajak Usaha', max_length=100)),
            ('rate', models.DecimalField(decimal_places=3, default=0.5, max_digits=6)),
            ('basis', models.CharField(choices=[('OMZET', 'Persentase omzet penjualan'), ('LABA', 'Persentase laba setelah biaya')], default='OMZET', max_length=10)),
            ('is_active', models.BooleanField(default=True)),
            ('note', models.CharField(blank=True, max_length=255)),
            ('updated_at', models.DateTimeField(auto_now=True)),
        ],
        options={'ordering': ['-is_active', 'name']},
    )]
