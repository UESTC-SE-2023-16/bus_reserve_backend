from django.db import models

# Create your models here.


class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    is_admin = models.BooleanField(default=False, editable=False)


class BusInfo(models.Model):
    id = models.AutoField(primary_key=True)
    busnum = models.CharField(max_length=32, unique=True)
    depart = models.CharField(max_length=32)
    destination = models.CharField(max_length=32)
    departtime = models.CharField(max_length=32)
    seats = models.IntegerField(default=35)
    remained_seats = models.PositiveIntegerField(default=35)
    fare = models.IntegerField(default=20)


class TicketStatus(models.TextChoices):
    SUBMIT = "S", "提交"
    INVALID = "I", "失效"
    NORMAL = "N", "正常"
    FINISHED = "F", "完成"
    TORIKESHI = "T", "取消"


class TicketInfo(models.Model):
    id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey("UserInfo", on_delete=models.CASCADE)
    b_id = models.ForeignKey("BusInfo", on_delete=models.CASCADE)
    # 车票状态默认为“提交”
    status = models.CharField(max_length=1, choices=TicketStatus.choices, default="S")
