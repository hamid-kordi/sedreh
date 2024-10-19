from celery import shared_task
from .models import User, OtpCode, Library
from book.models import Book
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


@shared_task
def celery_increaseـtheـbudget(username, code):
    try:
        otp_code = OtpCode.objects.filter(username=username, code=code)
        if otp_code.expiration_date < timezone.now():
            return {"status": "error", "message": "OTP code is expired."}
        user = User.objects.filter(username=username)
        user.budget += otp_code.price
        user.save()
    except OtpCode.DoesNotExist:
        return {"status": "error", "message": "Invalid OTP code."}
    except User.DoesNotExist:
        return {"status": "error", "message": "User not found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@shared_task
def celery_buy_book(user_id, book_id):
    try:
        user = User.objects.filter(user_id=user)
        book = Book.objects.get(id=book_id)
        if Library.objects.filter(book=book, user=user):
            return "This book is already in your library."
        if user.budget < book.price:
            return "Your budget is insufficient to buy this book."
        Library.objects.create(user=user, book=book)
        user.budget -= book.price
        user.save()
        return f"User {user.username} bought the book {book.name}."
    except User.DoesNotExist:
        return "User or book not found."
    except Exception as e:
        return str(e)


@shared_task
def celery_return_book(user_id, book_id):
    try:
        user = User.objects.get(id=user_id)
        book = Book.objects.get(id=book_id)

        library_entry = Library.objects.filter(user=user, book=book).first()
        if not library_entry:
            return "This book is not in your library."
        if timezone.now() - library_entry.added < timezone.timedelta(hours=1):
            user.budget += book.price
            user.save()
            library_entry.delete()

            return f"User {user.username} returned the book {book.name}."
        else:
            return "You can only return a book within one hour of purchase."
    except ObjectDoesNotExist:
        return "User or book not found."
    except Exception as e:
        return str(e)
