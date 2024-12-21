# Generated by Django 5.1.4 on 2024-12-20 21:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approval_chain', '0002_approvalstep_chain_approvalstep_status'),
        ('minutes', '0008_remove_minute_updated_at_minute_status_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='approvalstep',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='approvalstep',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='minute',
            name='approval_chain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='minutes', to='approval_chain.approvalchain'),
        ),
        migrations.AlterField(
            model_name='approvalstep',
            name='approver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='minute_approval_steps', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='approvalstep',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20),
        ),
        migrations.RemoveField(
            model_name='approvalstep',
            name='approved_at',
        ),
    ]