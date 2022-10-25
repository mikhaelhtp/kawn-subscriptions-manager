from django.test import TestCase, Client
from django.urls import reverse
# from kawn_subscriptions_manager.subscriptions.models import Subscription, SubscriptionPlan

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.list_subcriptions_plan_url = reverse("list_subscription_plan")

    def test_list_subscription_plan_template_sales(self):
        response  =self.client.get(self.list_subcriptions_plan_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'subscriptions/subscription_plans/sales/list_subscription_plan.html')