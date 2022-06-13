from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a user with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
        email=email,
        password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
 
class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField('Email', max_length = 100, default = "", blank = '', unique = True)
    name = models.CharField('Name', max_length = 100, default = "", blank = '', unique = True)
    password = models.CharField('Password', max_length = 256)
    is_admin = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    def create_user(self, **kwargs):
        some_salt = 'mMUj0DrIK6vgtdIYepkIxN'
        self.password = make_password(self.password, some_salt)
        super().save(**kwargs)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return self.id