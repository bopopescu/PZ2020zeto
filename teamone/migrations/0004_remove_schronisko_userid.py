# Generated by Django 2.2.8 on 2020-05-20 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teamone', '0003_schronisko_userid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schronisko',
            name='userID',
        ),
    ]