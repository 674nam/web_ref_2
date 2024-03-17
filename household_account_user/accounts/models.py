from django.db import models
# from django.contrib.auth.models import (BaseUserManager,
#                                         AbstractBaseUser,
#                                         PermissionsMixin)
from django.contrib.auth.models import BaseUserManager,AbstractUser
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields,
        )

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields['is_active'] = True
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields,
        )

# 世帯テーブル
class Family(models.Model):
    family_name = models.CharField(
            verbose_name=_("家名"),
            max_length=150,
            unique=True,
            null=True,
            blank=False
        )
    def __str__(self):
        return self.family_name

# カスタムユーザーモデル
class User(AbstractUser):
    username = models.CharField(
        verbose_name=_("ユーザー"),
        unique=True,
        max_length=10
    )
    email = models.EmailField(
        verbose_name=_("email"),
        unique=True
    )
    family_name = models.ForeignKey(
        Family,
        verbose_name=_("家名"),
        on_delete=models.CASCADE,
        null=True,
        default=None  # デフォルト値
    )
    first_name = models.CharField(
        verbose_name=_("名前"),
        max_length=150,
        null=True,
        blank=False
    )

    is_superuser = models.BooleanField(
        verbose_name=_("is_superuer"),
        default=False
    )
    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=True,
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_("created_at"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updateded_at"),
        auto_now=True
    )

    objects = UserManager()

    REQUIRED_FIELDS = ['email']  # スーパーユーザー作成時にemailも設定

    def __str__(self):
        return self.username