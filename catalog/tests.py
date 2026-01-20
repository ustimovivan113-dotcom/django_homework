from django.test import TestCase
from .models import Product

class ProductModelTest(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=100.00
        )
        self.assertEqual(product.name, "Test Product")