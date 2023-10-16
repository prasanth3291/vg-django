from django.db import models
from django.urls import reverse
from softdelete.models import SoftDeleteQuerySet, SoftDeleteManager


class category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    cat_image = models.ImageField(upload_to="pics/categories", blank=True)
    # add a sub category model

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def get_url(self):
        return reverse("product_by_category", args=[self.slug])

    def __str__(self):
        return self.category_name


class Sub_category(models.Model):
    sub_cat_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    categories = models.ManyToManyField(category, blank=True)

    def __str__(self):
        return self.sub_cat_name

    def get_url(self):
        return reverse("product_by_sub_category", args=[self.slug])


# Create your models here.
