# Generated by Django 3.0.6 on 2020-05-19 10:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0030_music_tag'),
        ('userprofile', '0002_auto_20200516_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikesAndDislikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('singer_disliked', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='singer_disliked', to='music.Singer')),
                ('singer_liked', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='singer_liked', to='music.Singer')),
                ('song_disliked', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='song_disliked', to='music.Music')),
                ('tag_disliked', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tag_disliked', to='music.MusicTag')),
                ('tag_liked', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tag_liked', to='music.MusicTag')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='likes_dislikes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
