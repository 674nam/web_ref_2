from django.db import models
# 現時点で有効になっているUserモデルの呼び出し
from django.contrib.auth import get_user_model
# 別アプリからの呼び出し：from アプリケーション名.models import クラス名
# 使用例）
# class Article(models.Model):
#     author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,)
from accounts.models import User

