from django.contrib.auth.models import User
from django.test import TestCase

from store.logic import set_rating
from store.models import Book, UserBookRelation


class SetRatingTestCase(TestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create(username='user_1', first_name='Ivan', last_name='Petrov')
        self.user2 = User.objects.create(username='user_2', first_name='Ivan', last_name='Sidorov')
        self.user3 = User.objects.create(username='user_3', first_name='1', last_name='2')

        self.book1 = Book.objects.create(name='Test book 1', price='1000', author_name='Author 1')

        UserBookRelation.objects.create(user=self.user1, book=self.book1, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user2, book=self.book1, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user3, book=self.book1, like=True, rate=4)

        UserBookRelation.objects.create(user=self.user3, book=self.book1, like=False)

    def test_ok(self):
        set_rating(self.book1)
        self.book1.refresh_from_db()
        self.assertEquals(str(self.book1.rating), '4.67')




