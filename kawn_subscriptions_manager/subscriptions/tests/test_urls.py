from django.test import SimpleTestCase
from django.urls import reverse, resolve
from kawn_subscriptions_manager.subscriptions.views import (
    ListSubscriptionPlan,
    AddSubscriptionPlan,
    UpdateSubscriptionPlan,
    DeleteSubscriptionPlan,
    activate_subscription_plan,
    deactivate_subscription_plan,
    ListSubscription,
    AddSubscription,
    UpdateSubscription,
    deactivate_subscription,
)


class TestUrls(SimpleTestCase):
    def test_list_subscription_plan_url_resolves(self):
        url = reverse("subscriptions:list_subscription_plan")
        self.assertEquals(resolve(url).func.view_class, ListSubscriptionPlan)

    def test_add_subscription_plan_url_resolves(self):
        url = reverse("subscriptions:add_subscription_plan")
        self.assertEquals(resolve(url).func.view_class, AddSubscriptionPlan)

    def test_update_subscription_plan_url_resolves(self):
        url = reverse("subscriptions:update_subscription_plan", args=(1,))
        self.assertEquals(resolve(url).func.view_class, UpdateSubscriptionPlan)

    def test_delete_subscription_plan_url_resolves(self):
        url = reverse("subscriptions:delete_subscription_plan", args=(1,))
        self.assertEquals(resolve(url).func.view_class, DeleteSubscriptionPlan)

    def test_activate_subscription_plan_url_resolves(self):
        url = reverse("subscriptions:activate_subscription_plan", args=(1,))
        self.assertEquals(resolve(url).func, activate_subscription_plan)

    def test_deactivate_subscription_plan_url_resolves(self):
        url = reverse("subscriptions:deactivate_subscription_plan", args=(1,))
        self.assertEquals(resolve(url).func, deactivate_subscription_plan)

    def test_list_subscription_url_resolves(self):
        url = reverse("subscriptions:list_subscription")
        self.assertEquals(resolve(url).func.view_class, ListSubscription)

    def test_add_subscription_url_resolves(self):
        url = reverse("subscriptions:add_subscription")
        self.assertEquals(resolve(url).func.view_class, AddSubscription)

    def test_update_subscription_url_resolves(self):
        url = reverse("subscriptions:update_subscription", args=(1,))
        self.assertEquals(resolve(url).func.view_class, UpdateSubscription)

    def test_deactivate_subscription_url_resolves(self):
        url = reverse("subscriptions:deactivate_subscription", args=(1,))
        self.assertEquals(resolve(url).func, deactivate_subscription)