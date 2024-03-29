# Generated by Django 4.2.4 on 2024-02-18 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_remove_user_details_city_category_view_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100, unique=True)),
            ],
        ),

        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['display_order', 'name']},
        ),
        migrations.AlterModelOptions(
            name='menu_item',
            options={'ordering': ['display_order', 'name']},
        ),
        migrations.AddField(
            model_name='category',
            name='display_order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='menu_item',
            name='display_order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('cash', 'Cash'), ('cart', 'Cart')], default='cash', max_length=10),
        ),
        migrations.AlterField(
            model_name='menu_item',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='menu_item',
            name='image',
            field=models.FileField(upload_to='menu_images/'),
        ),

    ]
