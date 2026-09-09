from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Harvest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.CharField(max_length=255)),
                ('quantity_kg', models.DecimalField(decimal_places=2, max_digits=12)),
                ('moisture', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
            options={'ordering': ['-date']},
        ),
    ]
