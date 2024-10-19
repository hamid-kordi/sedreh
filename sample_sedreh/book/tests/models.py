from django.test import TestCase
from .models import Category, Book

class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Fiction",
            slug="fiction",
            is_sub=False
        )

    def test_category_creation(self):
        self.assertIsInstance(self.category, Category)
        self.assertEqual(str(self.category), "Fiction")
        self.assertEqual(self.category.slug, "fiction")
        self.assertFalse(self.category.is_sub)

class BookModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Fiction",
            slug="fiction"
        )
        self.book = Book.objects.create(
            name="Sample Book",
            slug="sample-book",
            image="path/to/image.jpg",  # Ensure this path exists or mock the file field
            description="A sample book description.",
            price=20,
            available=True,
            file="path/to/book.pdf"  # Ensure this path exists or mock the file field
        )
        self.book.category.add(self.category)

    def test_book_creation(self):
        self.assertIsInstance(self.book, Book)
        self.assertEqual(str(self.book), "Sample Book")
        self.assertEqual(self.book.price, 20)
        self.assertTrue(self.book.available)
        self.assertEqual(self.book.category.count(), 1)
        self.assertEqual(self.book.category.first(), self.category)

    def test_book_category_relation(self):
        self.assertIn(self.category, self.book.category.all())
