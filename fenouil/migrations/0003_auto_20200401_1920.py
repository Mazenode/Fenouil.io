# Generated by Django 3.0.4 on 2020-04-01 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fenouil', '0002_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='nombre_de_commandes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='client',
            name='somme_totale_depensee',
            field=models.IntegerField(default=0),
        ),
    ]
