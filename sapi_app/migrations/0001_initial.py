# Generated by Django 2.2.3 on 2020-02-02 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APIKey',
            fields=[
                ('email', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('apikey', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='JSONRecord',
            fields=[
                ('record_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('json_string', models.TextField()),
                ('user_api_key', models.CharField(max_length=20)),
            ],
        ),
    ]
