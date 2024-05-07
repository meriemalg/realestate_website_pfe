# Generated by Django 5.0.4 on 2024-04-16 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0004_order_transaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='last_answer',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='response_content',
            field=models.TextField(default=''),
        ),
    ]
