# Generated by Django 3.0.6 on 2020-05-16 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatar/default.jpg', upload_to='avatar/%Y%m%d/'),
        ),
    ]