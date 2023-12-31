# Generated by Django 4.2.2 on 2023-06-23 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_classifieds_user"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ClassifiedsTypes",
            new_name="ClassifiedsType",
        ),
        migrations.AddField(
            model_name="category",
            name="child_category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.category",
            ),
        ),
        migrations.AddField(
            model_name="classifieds",
            name="slug",
            field=models.SlugField(default=None),
        ),
        migrations.AddField(
            model_name="classifieds",
            name="type",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.classifiedstype",
            ),
            preserve_default=False,
        ),
    ]
