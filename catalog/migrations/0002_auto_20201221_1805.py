# Generated by Django 3.1.2 on 2020-12-21 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(help_text='Enter a book genre.', max_length=200),
        ),
    ]