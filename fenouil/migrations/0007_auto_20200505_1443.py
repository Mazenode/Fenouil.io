# Generated by Django 2.1.5 on 2020-05-05 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fenouil', '0006_individu_nom_complet'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommandeCarteBancaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_reglement', models.CharField(max_length=20)),
                ('montant', models.IntegerField()),
                ('valide', models.CharField(max_length=20)),
                ('pub_date', models.DateTimeField(default=None, verbose_name='Date de création')),
                ('num_carte', models.IntegerField()),
                ('date_expiration', models.DateTimeField(default=None, verbose_name="Date d'expiration")),
                ('carte_valide', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CommandeCheque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_reglement', models.CharField(max_length=20)),
                ('montant', models.IntegerField()),
                ('valide', models.CharField(max_length=20)),
                ('pub_date', models.DateTimeField(default=None, verbose_name='Date de création')),
                ('num_cheque', models.IntegerField()),
                ('nom_banque', models.CharField(max_length=100)),
                ('signe', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ItemCommande',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.IntegerField(default=0)),
                ('item_existant', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='article', to='fenouil.Item')),
            ],
        ),
        migrations.DeleteModel(
            name='Envoi',
        ),
        migrations.RemoveField(
            model_name='anomalie',
            name='description',
        ),
        migrations.AddField(
            model_name='anomalie',
            name='individu',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='individu_commande', to='fenouil.Individu'),
        ),
        migrations.AlterField(
            model_name='anomalie',
            name='statut',
            field=models.CharField(max_length=200),
        ),
        migrations.AddField(
            model_name='commandecheque',
            name='articles',
            field=models.ManyToManyField(to='fenouil.ItemCommande'),
        ),
        migrations.AddField(
            model_name='commandecheque',
            name='individu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fenouil.Individu'),
        ),
        migrations.AddField(
            model_name='commandecartebancaire',
            name='articles',
            field=models.ManyToManyField(to='fenouil.ItemCommande'),
        ),
        migrations.AddField(
            model_name='commandecartebancaire',
            name='individu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fenouil.Individu'),
        ),
    ]
