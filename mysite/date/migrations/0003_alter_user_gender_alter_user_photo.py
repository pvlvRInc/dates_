# Generated by Django 4.0.3 on 2022-03-23 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('date', '0002_user_matches'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, upload_to='media/%Y/%m/%d'),
        ),
    ]
