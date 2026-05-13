from django.core.management.base import BaseCommand

from apps.payments.models import PaymentProduct

DEFAULT_PRODUCTS = [
    {"code": "DOC_1", "name": "Doc Pack", "description": "1 credit", "price_mad": "5.00", "credits": 1, "sort_order": 1},
    {"code": "MINI_10", "name": "Mini Pack", "description": "10 credits", "price_mad": "19.00", "credits": 10, "sort_order": 2},
    {"code": "PRO_30", "name": "Pro Pack", "description": "30 credits", "price_mad": "49.00", "credits": 30, "sort_order": 3},
    {"code": "SME_100", "name": "SME Pack", "description": "100 credits", "price_mad": "99.00", "credits": 100, "sort_order": 4},
]


class Command(BaseCommand):
    help = "Seed default payment products"

    def handle(self, *args, **options):
        for product in DEFAULT_PRODUCTS:
            PaymentProduct.objects.get_or_create(code=product["code"], defaults=product)
        self.stdout.write(self.style.SUCCESS("Payment products seeded."))
