# Generated by Django 2.1.5 on 2020-04-26 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fenouil', '0005_cibleroutage_statut'),
    ]

    operations = [
        migrations.AddField(
            model_name='individu',
            name='nom_complet',
            field=models.CharField(default='test', max_length=100),
            preserve_default=False,
        ),
    ]
