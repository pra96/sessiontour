# Generated by Django 3.2.6 on 2021-08-29 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_guide',
            field=models.BooleanField(default=True),
        ),
    ]