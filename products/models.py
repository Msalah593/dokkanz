from django.db import models
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models import signals
from .validators import price_validator
# Create your models here.


class Category(models.Model):
    name = models.CharField(unique=True, max_length=250,
                            null=False, blank=False)
    parent_category = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True,
        null=True,
        related_name='sub_categories')

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_sub_categories(self):
        if self.sub_categories.count == 0:
            return []
        sub_categories = self.sub_categories.all()
        return [{'id': n.id,
                 'name': n.name,
                 'sub_categories': n.get_sub_categories()}
                for n in sub_categories]

    def get_parent_category(self, id):
        if not self.parent_category.parent_category:
            return None
        if self.parent_category.parent_category.id == id:
            raise ValidationError(
                "Category cannot be child of it's own children")
        return self.parent_category.get_parent_category(id)


@receiver(signals.pre_save, sender=Category)
def category_parent_validator(sender, instance, update_fields, **kwargs):
    print(instance.parent_category)
    if instance.parent_category:
        if instance.id == instance.parent_category.id:
            raise ValidationError("Category cannot be it's own parent")

        instance.get_parent_category(instance.id)


class Product(models.Model):
    product_code = models.CharField(
        unique=True, max_length=200, null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    price = models.DecimalField(
        max_digits=12, decimal_places=2, null=False,
        blank=False, validators=[price_validator])
    quantity = models.PositiveIntegerField(null=False, blank=False)
    categories = models.ManyToManyField(
        Category, default=None, blank=True)

    def __str__(self):
        return self.name
