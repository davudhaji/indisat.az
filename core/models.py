from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=150)
    child_category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, blank=True, null=True
    )


class Country(models.Model):
    name = models.CharField(max_length=150)


class ChildCategory(models.Model):
    main_category = models.ForeignKey("Category", on_delete=models.CASCADE)
    name = models.CharField(max_length=150)


class Classifieds(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(ChildCategory, on_delete=models.CASCADE)
    Country = models.ForeignKey(Country, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    content = models.TextField()
    phone_number = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    expire_date = models.DateTimeField()  # created time + 15 days
    verify = models.BooleanField(default=False)
    slug = models.SlugField(default=None)
    type = models.ForeignKey("ClassifiedsType", on_delete=models.CASCADE)

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.title)
        self.expire_date = datetime.now() + timedelta(days=15)
        return super(Classifieds, self).save(*args, **kwargs)


class ClassifiedsUtils(models.Model):
    new = models.BooleanField(blank=True, null=True)
    delivery = models.BooleanField(blank=True, null=True)
    main_classifieds = models.ForeignKey(Classifieds, on_delete=models.CASCADE)


class ClassiFiedsStat(models.Model):
    views = models.IntegerField()
    classifieds = models.ForeignKey("Classifieds", on_delete=models.CASCADE)


class ClassifiedsType(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    bio = models.TextField()


class ExtraFields(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)


class ExtraValue(models.Model):
    value = models.CharField(max_length=120)
    field = models.ForeignKey("ExtraFields", on_delete=models.CASCADE)
    classifieds = models.ForeignKey("Classifieds", on_delete=models.CASCADE)


class Store(models.Model):
    name = models.CharField(max_length=100)
    store_bio = models.TextField()
