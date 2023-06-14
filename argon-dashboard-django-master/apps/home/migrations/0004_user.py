# Generated by Django 4.1.7 on 2023-05-02 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_remove_broker_broker_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=250)),
                ('email', models.CharField(default='', max_length=250, null=True)),
                ('contact_no', models.CharField(max_length=250)),
                ('user_password', models.CharField(max_length=250)),
                ('created_date', models.DateTimeField(null=True)),
                ('updated_date', models.DateTimeField(null=True)),
            ],
        ),
    ]
