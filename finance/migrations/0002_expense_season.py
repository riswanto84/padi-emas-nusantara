from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
    dependencies=[('finance','0001_initial'),('core','0001_initial')]
    operations=[migrations.AddField(model_name='expense',name='season',field=models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.PROTECT,related_name='finance_expenses',to='core.plantingseason'))]
