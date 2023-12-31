# Generated by Django 4.2.2 on 2023-06-15 18:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myauth", "0003_remove_childcategory_main_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="is_active",
            field=models.BooleanField(
                default=False,
                help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                verbose_name="active",
            ),
        ),
    ]
