# Generated by Django 5.1.4 on 2024-12-18 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(blank=True, choices=[('Admin', 'Admin'), ('Superuser', 'Superuser'), ('Faculty', 'Faculty')], max_length=20, null=True),
        ),
    ]