# Generated by Django 3.0.2 on 2020-05-05 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shumeipai', '0003_shumeipai_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='shumeipai',
            name='remarks',
            field=models.CharField(default='暂无备注', max_length=200),
        ),
    ]
