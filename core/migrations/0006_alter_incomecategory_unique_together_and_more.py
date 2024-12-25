# Generated by Django 5.1.4 on 2024-12-25 03:13

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_income_end_at_alter_incomecategory_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='incomecategory',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='income',
            name='end_at',
            field=models.DateField(blank=True, db_index=True, default=datetime.datetime(2025, 1, 24, 3, 13, 18, 263895, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.RemoveField(
            model_name='incomecategory',
            name='user',
        ),
        migrations.AddField(
            model_name='incomecategory',
            name='user',
            field=models.ManyToManyField(related_name='income_categories', to=settings.AUTH_USER_MODEL),
        ),
    ]
