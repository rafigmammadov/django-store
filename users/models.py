from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='users_profile_images', null=True, blank=True)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'Email verification for user {self.user.email}'

    def send_verification_email(self):
        send_mail(
            "Subject here",
            "Here is the message.",
            "from@example.com",
            [{self.user.email}],
            fail_silently=False,
        )
