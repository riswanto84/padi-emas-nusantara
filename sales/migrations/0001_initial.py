from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('customer', models.CharField(max_length=120)),
                ('product', models.CharField(default='Gabah', max_length=80)),
                ('quantity_kg', models.DecimalField(decimal_places=2, max_digits=12)),
                ('price_per_kg', models.DecimalField(decimal_places=2, max_digits=12)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('status', models.CharField(choices=[('LUNAS', 'Lunas'), ('SEBAGIAN', 'Sebagian'), ('BELUM', 'Belum Lunas')], default='BELUM', max_length=10)),
            ],
            options={'ordering': ['-date']},
        ),
    ]
