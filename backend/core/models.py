from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group
from django.utils import timezone
from django.conf import settings
from backend.storage_backends import PrivateMediaStorage
from django.core.files.storage import FileSystemStorage
import uuid
# Create your models here.


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a new user"""
        if not email:
            raise ValueError('Users must have an email address.')

        # Making the email in lowercase
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        # self._db to add multiple dbs
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """Create and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # Assign UserManager to Custom User Model

    USERNAME_FIELD = 'email'


def select_storage():
    return PrivateMediaStorage() if settings.USE_S3 else FileSystemStorage()


class File(models.Model):
    # file = models.FileField(upload_to ='_uploads/')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(storage=select_storage)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.file)
