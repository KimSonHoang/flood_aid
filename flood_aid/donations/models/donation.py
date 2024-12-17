from django.db import models

from .campaign import Campaign


class Donation(models.Model):
    PAYMENT_METHODS = [
        ("bank_transfer", "Chuyển khoản ngân hàng"),
        ("e_wallet", "Ví điện tử"),
        ("credit_card", "Thẻ tín dụng"),
        ("cash", "Tiền mặt"),
    ]

    donor = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.email} - {self.amount} - {self.campaign.title}"
