from django.db import models
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin)
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def _create_user(self, email, account_id, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, account_id=account_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, account_id, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email=email,
            account_id=account_id,
            password=password,
            **extra_fields,
        )

    def create_superuser(self, email, account_id, password, **extra_fields):
        extra_fields['is_active'] = True
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(
            email=email,
            account_id=account_id,
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
        return f'{str(self.id)} , {self.family_name}'

# カスタムユーザーモデル
class User(AbstractBaseUser, PermissionsMixin):
    account_id = models.CharField(
        verbose_name=_("account_id"),
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

    USERNAME_FIELD = 'account_id' # ログイン時、ユーザー名の代わりにaccount_idを使用
    REQUIRED_FIELDS = ['email']  # スーパーユーザー作成時にemailも設定

    def __str__(self):
        return f'{str(self.id)} , {self.account_id}'