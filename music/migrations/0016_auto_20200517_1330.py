# Generated by Django 3.0.6 on 2020-05-17 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0015_singer_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='singer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Singer'),
        ),
    ]
