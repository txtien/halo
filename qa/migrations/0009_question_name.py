# Generated by Django 3.0.6 on 2020-05-14 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0008_auto_20200514_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='name',
            field=models.CharField(default='a', max_length=100),
        ),
    ]
