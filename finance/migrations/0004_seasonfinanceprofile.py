from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [('finance', '0003_taxprofile'), ('core', '0001_initial')]
    operations = [migrations.CreateModel(
        name='SeasonFinanceProfile',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('opening_cash', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
            ('fixed_assets', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
            ('other_assets', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
            ('liabilities', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
            ('note', models.TextField(blank=True)),
            ('updated_at', models.DateTimeField(auto_now=True)),
            ('season', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='finance_profile', to='core.plantingseason')),
        ],
        options={'verbose_name': 'Profil Keuangan Musim Tanam', 'verbose_name_plural': 'Profil Keuangan Musim Tanam'},
    )]
