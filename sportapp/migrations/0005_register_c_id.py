# Generated by Django 2.2.6 on 2024-04-10 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportapp', '0004_addpage_page_seo'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='c_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
