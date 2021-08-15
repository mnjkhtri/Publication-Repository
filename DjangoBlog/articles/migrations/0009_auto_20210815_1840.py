# Generated by Django 3.2.4 on 2021-08-15 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_auto_20210808_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='doi',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='article',
            name='impactFactor',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='journal_type',
            field=models.CharField(choices=[('National', 'National'), ('International', 'International')], default='National', max_length=20),
        ),
        migrations.AddField(
            model_name='article',
            name='peer_reviewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='sjrRating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='doi',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='conferencearticle',
            name='doi',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='article',
            name='article_link',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_link',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='conferencearticle',
            name='conference_link',
            field=models.URLField(blank=True),
        ),
    ]
