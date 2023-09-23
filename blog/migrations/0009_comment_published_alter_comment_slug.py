# Generated by Django 4.1.7 on 2023-06-16 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_comment_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='published',
            field=models.DateTimeField(blank=True, help_text='The date & time this article was published', null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='slug',
            field=models.SlugField(unique=True, unique_for_date='published'),
        ),
    ]
