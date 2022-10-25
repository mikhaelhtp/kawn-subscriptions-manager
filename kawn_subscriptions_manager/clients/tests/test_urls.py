# from django.test import SimpleTestCase
# from django.urls import reverse, resolve
# from kawn_subscriptions_manager.clients.views import (
#     ListClient,
#     AddClient,
#     UpdateClient,
#     DeleteClient,
#     deactivate_client,
#     ListOutlet, 
#     AddOutlet,
# )


# class TestUrls(SimpleTestCase):
#     def test_list_url_resolves(self):
#         url = reverse("clients:list_client")
#         # print(resolve(url))
#         self.assertEquals(resolve(url).func.view_class, ListClient)

#     def test_add_url_resolves(self):
#         url = reverse("clients:add_client")
#         self.assertEquals(resolve(url).func.view_class, AddClient)

#     def test_update_url_resolves(self):
#         url = reverse("clients:update_client", args=(1,))
#         self.assertEquals(resolve(url).func.view_class, UpdateClient)

#     def test_delete_url_resolves(self):
#         url = reverse("clients:delete_client", args=(1,))
#         self.assertEquals(resolve(url).func.view_class, DeleteClient)

#     def test_deactivate_url_resolves(self):
#         url = reverse("clients:deactivate_client", args=(1,))
#         self.assertEquals(resolve(url).func, deactivate_client)

#     def test_list_outlet_url_resolves(self):
#         url = reverse("clients:list_outlet_client", args=(1,))
#         self.assertEquals(resolve(url).func.view_class, ListOutlet)

#     def test_add_outlet_url_resolves(self):
#         url = reverse("clients:add_outlet_client", args=(1,))
#         self.assertEquals(resolve(url).func.view_class, AddOutlet)
