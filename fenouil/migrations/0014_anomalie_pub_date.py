# Generated by Django 2.1.5 on 2020-04-18 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fenouil', '0013_anomalie'),
    ]

    operations = [
        migrations.AddField(
            model_name='anomalie',
            name='pub_date',
            field=models.DateTimeField(default=None, verbose_name='Date de publication'),
        ),
    ]
