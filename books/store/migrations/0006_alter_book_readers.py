# Generated by Django 4.2.1 on 2023-05-22 08:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0005_book_readers_alter_book_owner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='readers',
            field=models.ManyToManyField(related_name='books', through='store.UserBookRelation', to=settings.AUTH_USER_MODEL),
        ),
    ]
