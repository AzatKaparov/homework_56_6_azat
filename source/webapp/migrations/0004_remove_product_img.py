# Generated by Django 2.2 on 2020-08-27 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_product_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='img',
        ),
    ]