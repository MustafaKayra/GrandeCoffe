# Generated by Django 5.0.6 on 2025-03-26 18:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_remove_shoppingcart_complete_shoppingcart_ordered'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderedCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('shoppingcart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shoppingcart')),
            ],
        ),
    ]
