# Generated by Django 5.0.3 on 2024-03-16 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
