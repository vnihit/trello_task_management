# Generated by Django 2.0.6 on 2019-03-10 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0005_auto_20190310_0112'),
    ]

    operations = [
        migrations.AddField(
            model_name='boards',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('archived', 'archived')], default='active', max_length=20),
        ),
    ]
