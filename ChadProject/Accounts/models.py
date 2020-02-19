from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# External Imports
from uuid import uuid4
from phonenumber_field.modelfields import PhoneNumberField

# Model Fields
# Django default user model fields :
# id : generated with UUID
# username
# email
# password
# is_staff
# is_active
# is_superuser
# date_joined
# Exta fields :
# Gender (choice)
# Phone Number
# Bio
# Followers
# Profile Picture

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('X', 'Prefer not to mention')
)


def pfp_directory(instance, filename):
    file_extension = filename.split('.')[-1]
    filename = f'ProfilePicture.{file_extension}'
    return f'photos/User-{instance.username}/{filename}'


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **args):
        if not username:
            raise ValueError('You need to have a valid username')
        elif not email:
            raise ValueError('You need  to have a valid email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **args
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **args):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Default fields
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # Additional fields
    gender = models.CharField(choices=GENDER, max_length=50, default='X', blank=True)
    phone_number = PhoneNumberField(blank=True)
    bio = models.CharField(max_length=322, blank=True)
    followers = models.ManyToManyField(
        "User", related_name="followings", blank=True)
    profile_picture = models.ImageField(upload_to=pfp_directory, blank=True, default='default-pfp.png')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)
    objects = UserManager()

    def __str__(self):
        return f'@{self.username}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse("Accounts:Profile", kwargs={"username": self.username})
    
    def get_all_posts(self) :
        return self.posts.all().order_by('-created_at')
    