from django.urls import reverse
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksAPITestCase(APITestCase):

    def setUp(self) -> None:
        self.book1 = Book.objects.create(name='Test book 1', price='1000')
        self.book2 = Book.objects.create(name='Test book 2', price='1000')
        self.serialized_data = BooksSerializer([self.book1, self.book2], many=True).data
        self.url = reverse('book-list')

    def test_response_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_get_page_data(self):
        response_data = self.client.get(self.url).data
