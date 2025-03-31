import random
from faker import Faker
from django.core.management.base import BaseCommand
from products.models import Category, Product

class Command(BaseCommand):
    help = "Generatess test products for databases"

    def handle(self, *args, **options):
        fake = Faker()

        categories = ["Fruits", "Vegetables", "Milk Products", "Bakings"]
        categories_objects = [Category.objects.get_or_create(name=c)[0] for c in categories]

        Product.objects.all().delete()

        for _ in range(50):
            Product.objects.create(name = str(fake.word()).capitalize(), 
                                   category=random.choice(categories_objects),
                                   nomenclature=fake.unique.uuid4(),
                                   description=fake.text(max_nb_chars=100),
                                   price = random.randint(1, 100),
                                   discount = random.randint(0,50),
                                   stock = random.randint(1, 1000),
                                   available = random.choice(["True", "False"]),
                                   rating = round(random.uniform(0.1, 5.0), 1),
                                   attributes = {"colour": fake.color_name()})

        self.stdout.write(self.style.SUCCESS("Successfully added 50 products!"))