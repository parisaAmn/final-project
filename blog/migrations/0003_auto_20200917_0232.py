# Generated by Django 3.1 on 2020-09-16 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200917_0226'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Myuser',
            new_name='user',
        ),
    ]