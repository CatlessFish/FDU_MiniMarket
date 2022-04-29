from django.db import models

# Create your models here.

from datetime import date
from pickle import NONE
from django.db import models
from django.contrib.auth.models import(
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

class SiteUserManager(BaseUserManager):
    def create_user(self, username, nickname, building_no, room_no, contact, password=None):
        """
        Creates and saves an user
        """
        if not username:
            raise ValueError("You must specify an unique username")
        
        user = self.model(
            username = username,
            nickname = nickname,
            building_no = building_no,
            room_no = room_no,
            contact = contact,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, nickname, building_no, room_no, contact, password=None):
        """
        Creates and save a superuser
        """
        user = self.model(
            username = username,
            nickname = nickname,
            building_no = building_no,
            room_no = room_no,
            contact = contact,
        )

        user.set_password(password)
        user.is_superuser = True # Superuser has all permissions.
        user.is_staff = True # Staff can log in to the admin site.
        # user.save(using=self.db)
        user.save()
        return user


class SiteUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name="用户名",
        max_length=100,
        unique=True,
        blank=False
    )
    nickname = models.CharField(
        verbose_name="昵称",
        unique=True,
        max_length=100,
        blank=False,
    )
    building_no = models.IntegerField(
        verbose_name="楼号",
        blank=False,
    )
    room_no = models.IntegerField(
        verbose_name="寝室号",
        blank=False,
    )
    contact = models.CharField(
        verbose_name="联系方式",
        max_length=100,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # Can log in to admin site?

    objects = SiteUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = ['nickname', 'building_no', 'room_no', 'contact',]

    def __str__(self):
        return self.nickname
