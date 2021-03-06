from operator import mod
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create a new user
class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('User must have an email address.')
        if not username:
            raise ValueError('User must have a username.')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_guide(self, email, username, password):
        user = self.create_user(self.normalize_email(email), username, password)
        user.is_guide = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(self.normalize_email(email), username, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Helper function for User class
def get_profile_image_path(self):
    return f'static/images/profile_image/{self.pk}/{"profile_image.png"}'


def get_default_profile_img():
    return f'static/images/logos/logo-art.png'


# Main site custom user class
class User(AbstractBaseUser):
    # Default User fields
    email = models.EmailField(verbose_name='email', max_length=150, unique=True)
    username = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, default="" ,null=False)
    last_name = models.CharField(max_length=50, null=True)

    # custom fields for User
    is_guide = models.BooleanField(default=True)
    is_client = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255,
                                      upload_to=get_profile_image_path,
                                      null=True,
                                      blank=True,
                                      default=get_default_profile_img)
    hide_email = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def get_profile_image(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_image/{self.pk}/'):]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
