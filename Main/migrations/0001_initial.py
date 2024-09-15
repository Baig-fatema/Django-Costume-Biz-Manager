# Generated by Django 5.1.1 on 2024-09-15 11:21

import colorfield.fields
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': '3. Category',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=250, unique=True)),
                ('customer_mobile', models.CharField(max_length=15, unique=True)),
                ('customer_address', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': '2. Customers',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=250, unique=True)),
                ('photo', models.ImageField(blank=True, upload_to='vendor/')),
                ('address', models.TextField(blank=True)),
                ('mobile', models.CharField(max_length=15, unique=True)),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': '1. Vendors',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('detail', models.TextField(blank=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('photo', models.ImageField(blank=True, upload_to='product/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.category')),
            ],
            options={
                'verbose_name_plural': '4. Products',
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('price', models.FloatField()),
                ('color', colorfield.fields.ColorField(blank=True, default='#000000', image_field=None, max_length=25, samples=None, verbose_name='Color')),
                ('total_amt', models.FloatField(editable=False)),
                ('pur_date', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Main.category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.product')),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Main.vendor')),
            ],
            options={
                'verbose_name_plural': '5. Purchases',
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('price', models.FloatField()),
                ('total_amt', models.FloatField(editable=False)),
                ('sale_date', models.DateTimeField(auto_now_add=True)),
                ('color', colorfield.fields.ColorField(blank=True, default='#000000', image_field=None, max_length=25, samples=None)),
                ('max_sale_qty', models.IntegerField(blank=True, editable=False, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Main.category')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Main.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.product')),
            ],
            options={
                'verbose_name_plural': '6. Sales',
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_quantity', models.IntegerField(default=0, null=True)),
                ('sale_quantity', models.IntegerField(default=0, null=True)),
                ('total_bal_qty', models.IntegerField()),
                ('sale_customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Main.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.product')),
                ('purchase', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Main.purchase')),
                ('sale', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Main.sales')),
                ('purchase_vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Main.vendor')),
            ],
            options={
                'verbose_name_plural': '8. Inventory',
            },
        ),
        migrations.CreateModel(
            name='Avail_Stocks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('Item_price', models.FloatField()),
                ('total_price', models.FloatField()),
                ('color', colorfield.fields.ColorField(blank=True, default='#000000', image_field=None, max_length=25, samples=None)),
                ('category', models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.category')),
                ('Item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.product')),
            ],
            options={
                'verbose_name_plural': '7. Stocks',
                'unique_together': {('Item', 'category')},
            },
        ),
    ]
