# Generated by Django 4.1.7 on 2023-07-20 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_alter_contact_banner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='banner',
        ),
        migrations.AddField(
            model_name='contact',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
