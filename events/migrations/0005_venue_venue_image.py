# Generated by Django 5.0.4 on 2024-07-09 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_venue_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='venue_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]