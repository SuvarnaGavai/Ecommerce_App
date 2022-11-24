# Generated by Django 3.2.13 on 2022-04-14 20:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customadmin', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('productId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customadmin.product')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('address1', models.CharField(blank=True, max_length=100)),
                ('address2', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=45)),
                ('state', models.CharField(blank=True, max_length=45)),
                ('country', models.CharField(blank=True, max_length=45)),
                ('zipcode', models.CharField(blank=True, max_length=45)),
                ('is_default', models.BooleanField(blank=True, default=False)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(blank=True, max_length=30)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('productId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customadmin.product')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
