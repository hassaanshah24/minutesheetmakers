from django.db import migrations, models
from django.db import transaction
import datetime

def backfill_unique_id(apps, schema_editor):
    # Get the Minute model from the historical models
    Minute = apps.get_model('minutes', 'Minute')
    with transaction.atomic():
        for minute in Minute.objects.filter(unique_id__isnull=True):
            now = datetime.datetime.now()
            minute.unique_id = f"MM-{now.year}-{now.strftime('%m%d')}-{minute.id:03}"
            minute.save()

class Migration(migrations.Migration):

    dependencies = [
        ('minutes', '0005_minute_unique_id'),  # Previous migration file
    ]

    operations = [
        migrations.RunPython(backfill_unique_id),  # Backfill unique_id
        migrations.AlterField(
            model_name='minute',
            name='unique_id',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
