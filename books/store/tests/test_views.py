from django.urls import reverse
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksAPITestCase(APITestCase):

    def setUp(self) -> None:
        self.book1 = Book.objects.create(name='Test book 1', price='1000', author_name='Test author 1')
        self.book2 = Book.objects.create(name='Test book 2', price='1000', author_name='Test author 2')
        self.serialized_data = BooksSerializer([self.book1, self.book2], many=True).data
        self.url = reverse('book-list')

    def test_response_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_get_page_data(self):
        response_data = self.client.get(self.url).data


class FilterBookAPITestCase(APITestCase):

    def setUp(self) -> None:
        self.book1 = Book.objects.create(name='Test book 1', price='900', author_name='author 1')
        self.book2 = Book.objects.create(name='Test book 2', price='100', author_name='author 5')
        self.book3 = Book.objects.create(name='Test book author 1', price='1010', author_name='author 2')

        self.url = reverse('book-list')

    def test_get_filter_search(self):
        response = self.client.get(self.url, data={'search': 'author 1'})
        serialized_data = BooksSerializer([self.book1, self.book3], many=True).data

        self.assertEquals(response.status_code, 200)
        print(response.data)
        print(serialized_data)
        self.assertEquals(serialized_data, response.data)

    # def test_get_filter_order_price(self):
    #     response = self.client.get(self.url, data={'ordering': 'price'})
    #     serialized_data = BooksSerializer([self.book2, self.book1, self.book3], many=True).data
    #     self.assertEquals(response.status_code, 200)
    #     #self.assertEquals(response.data, serialized_data)



