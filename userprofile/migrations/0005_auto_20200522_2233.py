# Generated by Django 3.0.6 on 2020-05-22 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0033_auto_20200522_2233'),
        ('userprofile', '0004_auto_20200520_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likesanddislikes',
            name='singer_disliked',
            field=models.ManyToManyField(blank=True, related_name='singer_disliked', to='music.Singer'),
        ),
        migrations.AlterField(
            model_name='likesanddislikes',
            name='singer_liked',
            field=models.ManyToManyField(blank=True, related_name='singer_liked', to='music.Singer'),
        ),
        migrations.AlterField(
            model_name='likesanddislikes',
            name='song_disliked',
            field=models.ManyToManyField(blank=True, related_name='song_disliked', to='music.Music'),
        ),
        migrations.AlterField(
            model_name='likesanddislikes',
            name='tag_disliked',
            field=models.ManyToManyField(blank=True, related_name='tag_disliked', to='music.MusicTag'),
        ),
        migrations.AlterField(
            model_name='likesanddislikes',
            name='tag_liked',
            field=models.ManyToManyField(blank=True, related_name='tag_liked', to='music.MusicTag'),
        ),
    ]
