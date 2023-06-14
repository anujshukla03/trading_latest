# Generated by Django 4.1.7 on 2023-05-02 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_tradingaccount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradingaccount',
            name='BrokerID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.broker'),
        ),
        migrations.AlterField(
            model_name='tradingaccount',
            name='UserID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.user'),
        ),
    ]
