# Generated by Django 5.0.4 on 2024-05-12 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('first_name', models.CharField(max_length=10)),
                ('last_name', models.CharField(max_length=10)),
                ('username', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=20)),
                ('password', models.CharField(max_length=15)),
                ('createdAtTime', models.TimeField(auto_now_add=True)),
                ('createdAtDate', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
