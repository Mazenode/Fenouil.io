# Generated by Django 3.0.4 on 2020-03-30 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('prix', models.FloatField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
    ]
