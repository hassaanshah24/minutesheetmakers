# Generated by Django 5.1.4 on 2024-12-19 20:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minutes', '0003_minute_approval_chain'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='minute',
            name='approval_chain',
        ),
        migrations.RemoveField(
            model_name='minute',
            name='approvers',
        ),
        migrations.RemoveField(
            model_name='minute',
            name='current_approver',
        ),
        migrations.RemoveField(
            model_name='minute',
            name='marked_to',
        ),
        migrations.RemoveField(
            model_name='minute',
            name='returned_to',
        ),
        migrations.AddField(
            model_name='minute',
            name='current_step',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.CreateModel(
            name='ApprovalStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_order', models.PositiveIntegerField()),
                ('approved', models.BooleanField(default=False)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('approver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approval_steps', to=settings.AUTH_USER_MODEL)),
                ('minute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approval_steps', to='minutes.minute')),
            ],
            options={
                'ordering': ['step_order'],
                'unique_together': {('minute', 'step_order')},
            },
        ),
    ]