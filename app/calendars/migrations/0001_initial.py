# Generated by Django 4.2.7 on 2024-10-22 19:55

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('schedule', '0014_use_autofields_for_pk'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('schedule.event',),
        ),
    ]