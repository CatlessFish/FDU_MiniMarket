from django.db import models
from accounts.models import SiteUser

# Create your models here.

class Record(models.Model):
    is_want = models.BooleanField(
        verbose_name="是否是一个需求帖",
        default=True,
    )
    want = models.CharField(
        max_length=200,
        verbose_name="想换到的物品描述、数量",
        blank=False,
    )
    offer = models.CharField(
        max_length=200,
        verbose_name="可以用于交换的物品描述、数量",
        blank=False,
    )
    note = models.CharField(
        max_length=300,
        verbose_name="备注",
        blank=True,
    )
    update_time = models.DateTimeField(
        auto_now=True,
    )
    created_by = models.ForeignKey(
        SiteUser,
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self) -> str:
        return '想要：' + str(self.want)


class Subscribe(models.Model):
    record = models.ForeignKey(
        Record,  
        on_delete=models.CASCADE,
    )
    created_by = models.ForeignKey(
        SiteUser,
        on_delete=models.CASCADE,
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
    )
    comment = models.CharField(
        max_length=100,
        verbose_name="留言",
    )
