from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]
        db_table = "categories" 

class Product(models.Model):
    name = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )
    nomenclature = models.CharField(unique=True, max_length=50)
    image = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.FloatField(default=0.0)
    attributes = models.JSONField(default=dict)
    discount = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} ({self.nomenclature})'

    class Meta:
        ordering = ["-created_at"]
        db_table = "products"
        unique_together = ["name", "description"]
        