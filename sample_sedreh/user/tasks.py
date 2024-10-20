from celery import shared_task
from .models import User, OtpCode, Library
from book.models import Book
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


@shared_task
def celery_increaseـtheـbudget(user_id, code):
    try:
        otp_code = OtpCode.objects.get(user=user_id, code=code)
        if otp_code.expiration_date < timezone.now():
            return {"status": "error", "message": "OTP code is expired."}
        user = otp_code.user
        user.budget += otp_code.price
        user.save()
        otp_code.delete()
        return {"status": "success", "message": "Budget increased successfully."}
    except OtpCode.DoesNotExist:
        return {"status": "error", "message": "Invalid OTP code."}
    except User.DoesNotExist:
        return {"status": "error", "message": "User not found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


####
@shared_task
def celery_buy_book(username, book_id):
    try:
        user = User.objects.filter(username=username).first()
        book = Book.objects.filter(id=book_id)
        user_id = user.id
        if Library.objects.filter(user=user_id, book=book_id).exists():
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
def celery_return_book(username, book_id):
    try:
        user = User.objects.get(username=username)
        book = Book.objects.get(id=book_id)
        user_id = user.id
        library_entry = Library.objects.filter(user=user_id, book=book_id).first()
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
