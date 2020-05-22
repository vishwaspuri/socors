from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import uuid
from django.core.validators import MaxValueValidator, RegexValidator

class UserManager(BaseUserManager):
    def create_user(self, email, full_name,ph_number,password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            ph_number=ph_number,
            full_name=full_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, full_name,ph_number,password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            full_name=full_name,
            ph_number=ph_number,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, ph_number,password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            full_name=full_name,
            ph_number=ph_number,
            password=password,

        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user




class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,)
    full_name = models.CharField(max_length=60, unique=False, null=False)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    ph_number = models.CharField(max_length=10, unique=True)
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','ph_number'] # Email & Password are required by default.
    def get_full_name(self):
        # The user is identified by their email address
        return self.full_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

    objects = UserManager()


class Address(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
    city=models.CharField(max_length=150)
    area=models.CharField(max_length=500)
    street=models.CharField(max_length=150)
    state=models.CharField(max_length=25)
    pincode=models.IntegerField(validators=[MaxValueValidator(999999)])


class PhoneOTP(models.Model):
    phone_regex  = RegexValidator(regex=r'^\(|\)|\d{10}$', message='Phone number not correct!')
    phone        = models.CharField(validators=[phone_regex], max_length=10)
    otp          = models.CharField(max_length= 9, blank= True, null=True)
    count        = models.IntegerField(default=0)
    validated    = models.BooleanField(default=False)

    def __str__(self):
        return str(self.phone)+' is sent '+str(self.otp)

class LoginOTP(models.Model):
    phone_regex  = RegexValidator(regex=r'^\(|\)|\d{10}$', message='Phone number not correct!')
    phone        = models.CharField(validators=[phone_regex], max_length=10)
    otp          = models.CharField(max_length= 9, blank= True, null=True)
    count        = models.IntegerField(default=0)
    validated    = models.BooleanField(default=False)

    def __str__(self):
        return str(self.phone)+' is sent '+str(self.otp)