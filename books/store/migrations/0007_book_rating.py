# Generated by Django 4.2.1 on 2023-05-22 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_book_readers'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=3, null=True),
        ),
    ]
