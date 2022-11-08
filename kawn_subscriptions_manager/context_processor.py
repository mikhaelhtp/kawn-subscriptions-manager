from kawn_subscriptions_manager.subscriptions.models import Subscription
from django.db.models import Q


def notification(request):
    return {
        "bell": Subscription.objects.filter(is_approved=None).count(),
        "notif": Subscription.objects.filter(is_approved=None).order_by("-modified"),
        "notif_empty": Subscription.objects.filter(is_approved=None).count(),
        "sales_notif": Subscription.objects.filter(Q(active__isnull=False) | Q(is_approved__isnull=False)).order_by("-modified"),
    }
