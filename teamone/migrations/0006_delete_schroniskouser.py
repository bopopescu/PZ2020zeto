# Generated by Django 2.2.8 on 2020-05-20 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_email_max_length'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('authtoken', '0002_auto_20160226_1747'),
        ('teamone', '0005_schroniskouser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SchroniskoUser',
        ),
    ]