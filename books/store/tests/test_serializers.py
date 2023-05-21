from unittest import TestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksSerializerTestCase(TestCase):

    def setUp(self) -> None:
        self.book1 = Book.objects.create(name='Test book 1', price='1000')
        self.book2 = Book.objects.create(name='Test book 2', price='1000')
        self.data = BooksSerializer([self.book1, self.book2], many=True).data

        self.excpected_data = [
            {
                'id': self.book1.id,
                'name': 'Test book 1',
                'price': '1000.00'
            },
            {
                'id': self.book2.id,
                'name': 'Test book 2',
                'price': '1000.00'
            }
        ]

    def test_ok(self):
        self.assertEquals(self.excpected_data, self.data)

