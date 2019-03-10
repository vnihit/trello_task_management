# Generated by Django 2.0.6 on 2019-03-10 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0006_boards_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='lists',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('archived', 'archived')], default='active', max_length=20),
        ),
    ]