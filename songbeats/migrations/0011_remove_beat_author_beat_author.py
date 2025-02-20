# Generated by Django 4.2.5 on 2023-10-06 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songbeats', '0010_remove_author_beat_beat_author_alter_beat_genre_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beat',
            name='author',
        ),
        migrations.AddField(
            model_name='beat',
            name='author',
            field=models.ManyToManyField(blank=True, null=True, to='songbeats.author', verbose_name='Исполнитель(исполнители) трека'),
        ),
    ]
