# Generated by Django 3.0.4 on 2020-04-01 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fenouil', '0004_auto_20200401_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='commentaires',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
