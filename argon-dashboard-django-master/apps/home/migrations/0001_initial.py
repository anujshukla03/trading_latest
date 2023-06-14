# Generated by Django 4.1.7 on 2023-05-01 10:49

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='brokers',
            fields=[
                ('broker_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('broker_name', models.CharField(max_length=255)),
                ('broker_logo', models.ImageField(default='', upload_to='')),
            ],
        ),
    ]
