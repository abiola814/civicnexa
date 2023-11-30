from django.db import models
from django.urls import reverse
import secrets

from profiling.models import UserProfile

from .paystack import PayStack
# Create your models here.

class Payment(models.Model):
    STATUSES = [
        ('completed', 'paid'),
        ('failed', 'failed'),
        ('pending', 'pending'),
        ('reversed', 'reversed')
    ]
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    # email = models.EmailField()
    ref = models.CharField(max_length=200)
    fee_type = models.CharField(max_length=200)
    # name = models.CharField(max_length=200)
    state_ID = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUSES, default='pending', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ("-date_created",)

    def __str__(self) -> str:
        return f"{self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(10)
            object_with_similar_ref = Payment.objects.filter(ref=ref).first()
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self):
        return self.amount * 100

    
    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            self.paystack_response = result
            if result["amount"] / 100 == self.amount:
                self.verified = True
            self.save()
            return True
        return False

    

# @staticmethod
#     def convert_kobo(amount: float) -> int:
#         """
#         paystack only accept kobo amount... there is a need
#         to convert naira NGN to kobo... this function does that
#         """
#         kobo_equivalent: int = int(amount * 100)
#         return kobo_equivalent
    
#     @staticmethod
#     def convert_naira(amount: int) -> float:
#         """
#         this methods convert the kobo amount given by paystack to NGN
#         takes kobo amount as input and returns the equivalen