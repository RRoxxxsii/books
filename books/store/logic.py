
from store.models import UserBookRelation
from django.db.models import Avg


def set_rating(book):
    rating = UserBookRelation.objects.filter(book=book).aggregate(rating=Avg('rate'))
    book.rating = rating['rating']
    book.save()

