# Generated by Django 4.1.7 on 2023-03-13 02:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_customer_delete_newsletter_guide_age_guide_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrolledhikers',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.customer'),
        ),
    ]