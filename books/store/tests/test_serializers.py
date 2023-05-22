from django.db.models import Count, Case, When, Avg
from rest_framework.test import APITestCase

from django.contrib.auth.models import User

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BooksSerializerTestCase(APITestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create(username='user_1', first_name='Ivan', last_name='Petrov')
        self.user2 = User.objects.create(username='user_2', first_name='Ivan', last_name='Sidorov')
        self.user3 = User.objects.create(username='user_3', first_name='1', last_name='2')

        self.book1 = Book.objects.create(name='Test book 1', price='1000', author_name='Author 1')
        self.book2 = Book.objects.create(name='Test book 2', price='1000', author_name='Author 2')

        UserBookRelation.objects.create(user=self.user1, book=self.book1, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user2, book=self.book1, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user3, book=self.book1, like=True, rate=4)

        UserBookRelation.objects.create(user=self.user1, book=self.book2, like=True, rate=3)
        UserBookRelation.objects.create(user=self.user2, book=self.book2, like=True, rate=4)
        UserBookRelation.objects.create(user=self.user3, book=self.book1, like=False)

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')).order_by('id')

        self.data = BooksSerializer(books, many=True).data

        self.expected_data = [
            {
                'id': self.book1.id,
                'name': 'Test book 1',
                'price': '1000.00',
                'author_name': 'Author 1',
                'annotated_likes': 3,
                'rating': '4.67',
                'owner_name': 'user1',
                'readers': [
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Petrov'
                    }
                ]
            },
            {
                'id': self.book2.id,
                'name': 'Test book 2',
                'price': '1000.00',
                'author_name': 'Author 2',
                'annotated_likes': 2,
                'rating': '3.50',
                'owner_name': '',
                'readers': [
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Sidorov'
                    }
                ]
            }
        ]

    def test_ok(self):
        print(self.expected_data)
        print(self.data)
        #self.assertEquals(self.expected_data, self.data)

