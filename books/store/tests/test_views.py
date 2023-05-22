import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from store.models import Book, UserBookRelation
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


class CRUDBookAPITest(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2', )
        self.user3 = User.objects.create(username='test_username3', is_staff=True)

        self.book1 = Book.objects.create(name='Test book 1', price='900', author_name='author 1', owner=self.user)
        self.book2 = Book.objects.create(name='Test book 2', price='100', author_name='author 5', owner=self.user)
        self.book3 = Book.objects.create(name='Test book author 1', price='1010', author_name='author 2', owner=self.user)

        self.client.force_login(self.user)

    def test_create(self):
        url = reverse('book-list')
        data = {'name': 'Programming in Python 3',
                'price': 150,
                'author_name': 'Mark Summerfield'}
        before_request = Book.objects.all().count()
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEquals(response.status_code, 201)
        after_request = Book.objects.all().count()
        self.assertEquals(before_request + 1, after_request)
        self.assertEquals(self.user, Book.objects.last().owner)

    def test_update_owner(self):

        url = reverse('book-detail', args=(self.book1.id,))
        data = {'name': self.book1.name,
                'price': 10,
                'author_name': self.book1.author_name}

        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json')

        self.book1.refresh_from_db()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(10, self.book1.price)

    def test_update_not_owner(self):

        self.client.force_login(self.user2)
        url = reverse('book-detail', args=(self.book1.id,))
        data = {'name': self.book1.name,
                'price': 900,
                'author_name': self.book1.author_name}

        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json')

        self.book1.refresh_from_db()
        self.assertEquals(response.status_code, 403)
        self.assertNotEquals(10, self.book1.price)

    def test_update_not_owner_but_stuff(self):
        self.client.force_login(self.user3)
        url = reverse('book-detail', args=(self.book1.id,))
        data = {'name': self.book1.name,
                'price': 900,
                'author_name': self.book1.author_name}

        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json')

        self.book1.refresh_from_db()
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(10, self.book1.price)

    def test_delete_owner(self):
        url = reverse('book-detail', args=(self.book1.id,))

        before_request = Book.objects.all().count()
        response = self.client.delete(url)

        after_request = Book.objects.all().count()
        self.assertEquals(before_request - 1, after_request)

    def test_delete_not_owner(self):
        self.client.force_login(self.user2)
        url = reverse('book-detail', args=(self.book1.id,))

        before_request = Book.objects.all().count()
        response = self.client.delete(url)

        after_request = Book.objects.all().count()

        self.assertEquals(response.status_code, 403)
        self.assertEquals(before_request, after_request)

    def test_delete_not_owner_but_stuff(self):
        self.client.force_login(self.user3)
        url = reverse('book-detail', args=(self.book1.id,))

        before_request = Book.objects.all().count()
        response = self.client.delete(url)

        after_request = Book.objects.all().count()

        self.assertEquals(response.status_code, 204)
        self.assertEquals(before_request - 1, after_request)


class BooksRelationTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2', )
        self.user3 = User.objects.create(username='test_username3', is_staff=True)

        self.book1 = Book.objects.create(name='Test book 1', price='900', author_name='author 1', owner=self.user)
        self.book2 = Book.objects.create(name='Test book 2', price='100', author_name='author 5', owner=self.user)
        self.book3 = Book.objects.create(name='Test book author 1', price='1010', author_name='author 2', owner=self.user)

    def test_like(self):
        self.client.force_login(self.user)

        data = {
                'like': True
                }
        json_data = json.dumps(data)

        url = reverse('userbookrelation-detail', args=[self.book1.id,])
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.book1.refresh_from_db()
        relation = UserBookRelation.objects.get(user=self.user, book=self.book1)

        self.assertEquals(response.status_code, 200)
        self.assertTrue(relation.like)

    def test_add_to_bookmarks(self):
        self.client.force_login(self.user)

        data = {
                'in_bookmarks': True
                }
        json_data = json.dumps(data)

        url = reverse('userbookrelation-detail', args=[self.book1.id,])
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.book1.refresh_from_db()
        relation = UserBookRelation.objects.get(user=self.user, book=self.book1)

        self.assertEquals(response.status_code, 200)
        self.assertTrue(relation.in_bookmarks)

    def test_rate(self):
        self.client.force_login(self.user)

        data = {
            'rate': 3
        }
        json_data = json.dumps(data)

        url = reverse('userbookrelation-detail', args=[self.book1.id, ])
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.book1.refresh_from_db()
        relation = UserBookRelation.objects.get(user=self.user, book=self.book1)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(relation.rate, 3)

    def test_rate_with_wrong_rate_value(self):
        self.client.force_login(self.user)

        data = {
            'rate': 6
        }
        json_data = json.dumps(data)

        url = reverse('userbookrelation-detail', args=[self.book1.id, ])
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.book1.refresh_from_db()
        relation = UserBookRelation.objects.get(user=self.user, book=self.book1)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(relation.rate, None)





