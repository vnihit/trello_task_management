from django.db import models
from django_mysql.models import ListTextField
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Boards(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=20)
    STATUS_CHOICES = [("active", "active"), ("archived", "archived")]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    labels = ListTextField(
        base_field=models.CharField(max_length=255), size=6, blank=True, null=True
    )  # max 6 labels per board

    def __str__(self):
        return str(self.name) + str(self.id)


class Lists(models.Model):
    name = models.CharField(max_length=20)
    board = models.ForeignKey(Boards, on_delete=models.CASCADE)
    STATUS_CHOICES = [("active", "active"), ("archived", "archived")]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    card_order = ListTextField(
        base_field=models.IntegerField(), size=100, blank=True, null=True
    )

    def __str__(self):
        return str(self.name)


class Cards(models.Model):
    title = models.CharField(max_length=20)
    list_instance = models.ForeignKey(Lists, on_delete=models.CASCADE)
    due_date = models.DateField(blank=True, null=True)
    label = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.title)


class Members(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
