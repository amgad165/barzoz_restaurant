# Generated by Django 4.2.4 on 2024-01-04 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_menu_item_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_details',
            name='city',
        ),
        migrations.AddField(
            model_name='category',
            name='view_homepage',
            field=models.BooleanField(default=False),
        ),
    ]
