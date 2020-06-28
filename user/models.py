from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import uuid
from django.core.validators import MaxValueValidator, RegexValidator
from django.dispatch import receiver
from allauth.account.signals import user_signed_up


class UserManager(BaseUserManager):
    def create_user(self, email, full_name,password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, full_name,password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name,password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            full_name=full_name,
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
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,)
    full_name    = models.CharField(max_length=60, unique=False, null=False)
    active       = models.BooleanField(default=True)
    staff        = models.BooleanField(default=False) # a admin user; non super-user
    admin        = models.BooleanField(default=False) # a superuser
    ph_number    = models.CharField(max_length=10)
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name'] # Email & Password are required by default.
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
    def to_dict(self):
        user_dict={
            'name': self.full_name,
            'email': self.email,
            'phone number': self.ph_number,
            'id': self.id
        }
        address_dict=[]
        addresses=self.address.all()
        for address in addresses:
            address_dict.append(address.to_dict())
        user_dict['addresses']=address_dict
        return user_dict

    objects = UserManager()

@receiver(user_signed_up)
def populate_soc_login_data(sociallogin,user,**kwargs):
    if sociallogin.account.provider == 'google':
        user.full_name=sociallogin.account.extra_data['name']
        user.save()
    elif sociallogin.account.provider=='facebook':
        user.full_name=sociallogin.account.extra_data['name']
        user.save()

class Address(models.Model):
    user          =models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
    city          =models.CharField(max_length=150)
    area          =models.CharField(max_length=500)
    street        =models.CharField(max_length=150)
    state         =models.CharField(max_length=25)
    pincode       =models.IntegerField(validators=[MaxValueValidator(999999)])
    is_main       =models.BooleanField(default=False)

    def class_name(self):
        return 'address'+str(self.id)

    def make_address_main(self):
        pass

    def to_dict(self):
        add_dict = {
            'city':self.city,
            'area': self.area,
            'street': self.street,
            'state': self.state,
            'pincode': self.pincode
        }
        return add_dict


class PhoneOTP(models.Model):
    phone_regex  = RegexValidator(regex=r'^\(|\)|\d{10}$', message='Phone number not correct!')
    phone        = models.CharField(validators=[phone_regex], max_length=10)
    # Email and fullnme fields
    email        = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True
    )
    full_name    = models.CharField(max_length=60, unique=False, null=True)
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





