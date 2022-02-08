# Generated by Django 3.2.4 on 2022-02-08 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='stock_manager.order'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='stock_manager.product'),
        ),
    ]
