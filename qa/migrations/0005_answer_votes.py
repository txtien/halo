# Generated by Django 3.0.6 on 2020-05-14 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0004_auto_20200514_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]
