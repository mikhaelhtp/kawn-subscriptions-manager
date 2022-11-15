from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from django.db.models import Q

from kawn_subscriptions_manager.subscriptions.models import Subscription
from kawn_subscriptions_manager.decorators import allowed_users

# Create your views here.


# class SubscriptionLogs(ListView):
#     model = Subscription
#     queryset = Subscription.objects.filter(
#         Q(created_by__isnull=False)
#         | Q(modified_by__isnull=False)
#         | Q(deleted_by__isnull=False)
#     ).order_by("-created", "-modified")
#     template_name = "dashboard/dashboard.html"

class SubscriptionLogsCreated(ListView):
    model = Subscription
    queryset = Subscription.objects.filter(created_by__isnull=False).order_by("-created")
    template_name = "dashboard/dashboard_logs_created.html"


class SubscriptionLogsModified(ListView):
    model = Subscription
    queryset = Subscription.objects.filter(modified_by__isnull=False).order_by("-modified")
    template_name = "dashboard/dashboard_logs_modified.html"
