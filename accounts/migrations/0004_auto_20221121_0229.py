# Generated by Django 3.2.13 on 2022-11-20 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20221121_0203'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='category',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='nid',
            field=models.IntegerField(default=0),
        ),
    ]
