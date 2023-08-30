# Generated by Django 4.1.3 on 2023-08-30 00:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=250)),
                ('shoe_size', models.CharField(max_length=5)),
                ('email', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.CharField(max_length=10000)),
                ('description', models.CharField(max_length=50)),
                ('condition', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('color', models.CharField(max_length=50)),
                ('brand', models.CharField(max_length=50)),
                ('seller_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_info', to='solehubapi.user')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField()),
                ('payment_type', models.CharField(max_length=10)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solehubapi.user')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solehubapi.order')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solehubapi.product')),
            ],
        ),
    ]
