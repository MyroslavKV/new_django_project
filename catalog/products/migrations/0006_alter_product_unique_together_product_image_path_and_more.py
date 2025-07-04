# Generated by Django 5.1.7 on 2025-06-17 17:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_payment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('name', 'nomenclature')},
        ),
        migrations.AddField(
            model_name='product',
            name='image_path',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.product'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='provider',
            field=models.CharField(choices=[('liqpay', 'LiqPay'), ('monopay', 'MonoPay'), ('googlepay', 'Google Pay')], max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='attributes',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('cart', 'product')},
        ),
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]
