from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
    dependencies=[('sales','0001_initial'),('core','0001_initial')]
    operations=[migrations.AddField(model_name='sale',name='season',field=models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.PROTECT,related_name='sales_sales',to='core.plantingseason'))]
