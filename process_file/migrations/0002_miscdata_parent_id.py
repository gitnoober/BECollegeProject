# Generated by Django 4.2 on 2023-04-29 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('process_file', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='miscdata',
            name='parent_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='process_file.miscdata'),
        ),
    ]
