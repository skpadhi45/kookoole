# Generated by Django 4.1.3 on 2023-02-03 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kookooleShop', '0004_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerPin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin', models.CharField(max_length=10)),
                ('post_name', models.CharField(default='', max_length=50)),
            ],
        ),
    ]
