# Generated by Django 2.0.6 on 2019-03-10 04:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0007_lists_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cards',
            old_name='list_name',
            new_name='list_instance',
        ),
    ]
