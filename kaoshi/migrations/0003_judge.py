# Generated by Django 2.1.7 on 2019-05-08 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaoshi', '0002_auto_20190508_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='Judge',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('topic', models.TextField()),
                ('key', models.BooleanField()),
            ],
        ),
    ]
