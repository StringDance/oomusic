# Generated by Django 3.0.6 on 2020-05-19 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0025_auto_20200519_1605'),
    ]

    operations = [
        migrations.CreateModel(
            name='MusicTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='SingerTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=4)),
            ],
        ),
    ]
