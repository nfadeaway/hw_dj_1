# Generated by Django 4.1.4 on 2023-01-26 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0003_favoriteadv'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favoriteadv',
            old_name='favorite_adv_id',
            new_name='favorite_adv',
        ),
    ]
