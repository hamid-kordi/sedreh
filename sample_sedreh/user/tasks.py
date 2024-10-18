from celery import shared_task
from .models import User, OtpCode
from book.models import Book



@shared_task
def celery_increaseـtheـbudget(user_id, code):
    pass

@shared_task
def celery_buy_book(user_id,book_id):
    pass

@shared_task
def celery_return_book(user_id,book_id):
    pass