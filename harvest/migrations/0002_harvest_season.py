from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
    dependencies=[('harvest','0001_initial'),('core','0001_initial')]
    operations=[migrations.AddField(model_name='harvest',name='season',field=models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.PROTECT,related_name='harvest_harvests',to='core.plantingseason'))]
