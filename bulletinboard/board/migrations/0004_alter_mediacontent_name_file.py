# Generated by Django 4.0.2 on 2022-02-19 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_responad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediacontent',
            name='name_file',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
