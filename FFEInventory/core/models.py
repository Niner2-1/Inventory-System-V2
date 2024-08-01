from django.db import models
from django.core.exceptions import ValidationError


class Branch(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Custody(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self) -> str:
        return self.title


class Item(models.Model):
    ITEM_TYPE_CHOICES = [
        ("system unit", "System Unit"),
        ("monitor", "Monitor"),
        ("printer", "Printer"),
        ("ups", "UPS"),
        ("hub", "Hub"),
    ]
    FFE_number = models.CharField(max_length=255, null=False, blank=False, unique=True)
    old_FFE = models.CharField(max_length=255, null=True, blank=True, unique=True)
    item_type = models.CharField(max_length=255, choices=ITEM_TYPE_CHOICES, null=False, blank=False)
    processor = models.CharField(max_length=255, null=True, blank=True)
    motherboard = models.CharField(max_length=255, null=True, blank=True)
    memory = models.CharField(max_length=255, null=True, blank=True)
    video_card = models.CharField(max_length=255, null=True, blank=True)
    hard_disk = models.CharField(max_length=255, null=True, blank=True)
    others = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    cost = models.CharField(max_length=255, null=True, blank=True)
    date_purchased = models.DateField()
    originating_branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="originating_branch")
    current_branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="current_branch")
    status = models.CharField(max_length=255, null=True, blank=True)
    custody = models.ForeignKey(Custody, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.FFE_number


class Transaction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=255, blank=True, null=True)
    remark = models.TextField()
    current_branch = models.CharField(max_length=255, null=True, blank=True)
    custody = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.item.FFE_number
