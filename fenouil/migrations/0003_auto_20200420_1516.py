# Generated by Django 2.1.5 on 2020-04-20 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fenouil', '0002_anomalie_envoi_individu_mail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individu',
            name='date',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
