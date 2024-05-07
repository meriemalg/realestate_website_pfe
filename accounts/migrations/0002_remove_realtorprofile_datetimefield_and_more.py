# Generated by Django 5.0.3 on 2024-04-02 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='realtorprofile',
            name='datetimefield',
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='background',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='perferances',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='search_history',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='realtorprofile',
            name='biographie',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='realtorprofile',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
