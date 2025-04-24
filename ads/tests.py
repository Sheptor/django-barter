from django.test import TestCase
from django.contrib.auth.models import User
from ads.forms import NewAdForm
from ads.models import Ad
from django.urls import reverse


class TestAds(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(username="test_user_1", password="test_user_password")
        self.user_2 = User.objects.create_user(username="test_user_2", password="test_user_password")
        self.client.force_login(self.user_1)

    def test_valid_form_with_image(self):
        form_data = {
            "title": "Test ad title.",
            "description": "Test ad description",
            "image_url": "https://www.python.org/static/img/python-logo.png",
            "category": "Test ad",
            "condition": "For tests only!"
        }
        form = NewAdForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_form_without_image(self):
        form_data = {
            "title": "Test ad title.",
            "description": "Test ad description",
            "image_url": "",
            "category": "Test ad",
            "condition": "For tests only!"
        }
        form = NewAdForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_without_title(self):
        form_data = {
            "title": "",
            "description": "Test ad description",
            "image_url": "",
            "category": "Test ad",
            "condition": "For tests only!"
        }
        form = NewAdForm(data=form_data)
        self.assertTrue(form.has_error("title"))
        self.assertFalse(form.is_valid())

    def test_invalid_form_without_description(self):
        form_data = {
            "title": "Test ad title.",
            "description": "",
            "image_url": "",
            "category": "Test ad",
            "condition": "For tests only!"
        }
        form = NewAdForm(data=form_data)
        self.assertTrue(form.has_error("description"))
        self.assertFalse(form.is_valid())

    def test_invalid_form_without_category(self):
        form_data = {
            "title": "Test ad title.",
            "description": "Test ad description",
            "image_url": "",
            "category": "",
            "condition": "For tests only!"
        }
        form = NewAdForm(data=form_data)
        self.assertTrue(form.has_error("category"))
        self.assertFalse(form.is_valid())

    def test_invalid_form_without_condition(self):
        form_data = {
            "title": "Test ad title.",
            "description": "Test ad description",
            "image_url": "",
            "category": "Test ad",
            "condition": ""
        }
        form = NewAdForm(data=form_data)
        self.assertTrue(form.has_error("condition"))
        self.assertFalse(form.is_valid())

    def test_invalid_image_url_form(self):
        form_data = {
            "title": "Test ad title.",
            "description": "Test ad description",
            "image_url": "not url",
            "category": "Test ad",
            "condition": "For tests only!"
        }
        form = NewAdForm(data=form_data)
        self.assertTrue(form.has_error("image_url"))
        self.assertFalse(form.is_valid())

    def test_create_view_with_correct_form_with_image_url(self):
        form_data = {
            "title": "Test ad title.",
            "description": "Test ad description",
            "image_url": "https://www.python.org/static/img/python-logo.png",
            "category": "Test ad",
            "condition": "For tests only!"
        }
        response_1 = self.client.post(reverse("ads:new_ad"), data=form_data)
        self.assertEqual(response_1.status_code, 302)
        self.assertRedirects(response_1, reverse("ads:ad_confirmation"))

        response_2 = self.client.post(reverse("ads:ad_confirmation"))
        self.assertEqual(response_2.status_code, 302)
        self.assertEqual(Ad.objects.last().title, "Test ad title.")
        self.assertEqual(Ad.objects.last().user, self.user_1)
        self.assertRedirects(response_2, reverse("ads:ad_detail", kwargs={"pk": Ad.objects.last().id}))

    def test_create_view_with_correct_form_without_image_url(self):
        form_data = {
            "title": "Test ad title.",
            "description": "Test ad description",
            "category": "Test ad",
            "condition": "For tests only!"
        }
        response_1 = self.client.post(reverse("ads:new_ad"), data=form_data)
        self.assertEqual(response_1.status_code, 302)
        self.assertRedirects(response_1, reverse("ads:ad_confirmation"))

        response_2 = self.client.post(reverse("ads:ad_confirmation"))
        self.assertEqual(response_2.status_code, 302)
        self.assertEqual(Ad.objects.last().title, "Test ad title.")
        self.assertEqual(Ad.objects.last().user, self.user_1)
        self.assertRedirects(response_2, reverse("ads:ad_detail", kwargs={"pk": Ad.objects.last().id}))

    def test_create_view_with_correct_form_without_login(self):
        self.client.logout()
        form_data = {
            "title": "Test ad title.",
            "description": "Test ad description",
            "image_url": "https://www.python.org/static/img/python-logo.png",
            "category": "Test ad",
            "condition": "For tests only!"
        }
        response_1 = self.client.post(reverse("ads:new_ad"), data=form_data)
        self.assertEqual(response_1.status_code, 302)
        self.assertRedirects(response_1, reverse("users:login"))

    def test_create_view_with_invalid_form_without_title(self):
        form_data = {
            "title": "",
            "description": "Test ad description",
            "category": "Test ad",
            "condition": "For tests only!"
        }
        response_1 = self.client.post(reverse("ads:new_ad"), data=form_data)
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(len(response_1.context["form"].errors), 1)
        self.assertEqual(response_1.context["form"].errors["title"][0], "Обязательное поле.")

    def test_create_view_with_invalid_form_without_description(self):
        form_data = {
            "title": "Test ad title.",
            "description": "",
            "category": "Test ad",
            "condition": "For tests only!"
        }
        response_1 = self.client.post(reverse("ads:new_ad"), data=form_data)
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(len(response_1.context["form"].errors), 1)
        self.assertEqual(response_1.context["form"].errors["description"][0], "Обязательное поле.")

    def test_create_view_with_invalid_form_without_category(self):
        form_data = {
            "title": "Test ad title.",
            "description": "Test ad description",
            "category": "",
            "condition": "For tests only!"
        }
        response_1 = self.client.post(reverse("ads:new_ad"), data=form_data)
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(len(response_1.context["form"].errors), 1)
        self.assertEqual(response_1.context["form"].errors["category"][0], "Обязательное поле.")

    def test_create_view_with_invalid_form_without_condition(self):
        form_data = {
            "title": "Test ad title.",
            "description": "Test ad description",
            "category": "Test ad",
            "condition": ""
        }
        response_1 = self.client.post(reverse("ads:new_ad"), data=form_data)
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(len(response_1.context["form"].errors), 1)
        self.assertEqual(response_1.context["form"].errors["condition"][0], "Обязательное поле.")

    def test_get_empty_ads_list(self):
        response = self.client.get(reverse("ads:ads"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["ads"]), 0)

    def test_get_many_ads_list(self):
        form_data = {
            "title": "Test ad title.",
            "description": "Test ad description",
            "image_url": "https://www.python.org/static/img/python-logo.png",
            "category": "Test ad",
            "condition": "For tests only!"
        }
        for i_index in range(20):
            Ad.objects.create(user=self.user_1, **form_data)

        response_1 = self.client.get(f"{reverse('ads:ads')}")
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(len(response_1.context["ads"]), 15)

        response_2 = self.client.get(f"{reverse('ads:ads')}?page=2")
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(len(response_2.context["ads"]), 5)

    def test_get_ad(self):
        form_data = {
            "title": "Test ad title.",
            "description": "Test ad description",
            "image_url": "https://www.python.org/static/img/python-logo.png",
            "category": "Test ad",
            "condition": "For tests only!"
        }
        Ad.objects.create(user=self.user_1, **form_data)
        response = self.client.get(reverse("ads:ad_detail", kwargs={"pk": Ad.objects.last().id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["ad"], Ad.objects.last())

    def test_get_unknown_ad(self):
        form_data = {
            "title": "Test ad title.",
            "description": "Test ad description",
            "image_url": "https://www.python.org/static/img/python-logo.png",
            "category": "Test ad",
            "condition": "For tests only!"
        }
        Ad.objects.create(user=self.user_1, **form_data)
        response = self.client.get(reverse("ads:ad_detail", kwargs={"pk": Ad.objects.last().id + 1}))
        self.assertEqual(response.status_code, 404)

    def test_update_ad_with_correct_form(self):
        form_data = {
            "title": "Test ad title.",
            "description": "Test ad description",
            "image_url": "https://www.python.org/static/img/python-logo.png",
            "category": "Test ad",
            "condition": "For tests only!"
        }
        Ad.objects.create(user=self.user_1, **form_data)
        form_new_data = {
            "title": "New test ad title.",
            "description": "New test ad description",
            "image_url": "https://www.python.org/static/img/psf-logo.png",
            "category": "New test ad",
            "condition": "New for tests only!",
            "_method": "PUT"
        }
        response_1 = self.client.post(reverse("ads:ad_edit", kwargs={"pk": Ad.objects.last().id}), form_new_data)
        self.assertEqual(response_1.status_code, 302)
        self.assertRedirects(response_1, reverse("ads:ad_detail", kwargs={"pk": Ad.objects.last().id}))

        response_2 = self.client.get(reverse("ads:ad_detail", kwargs={"pk": Ad.objects.last().id}))
        self.assertEqual(response_2.context["ad"].title, form_new_data["title"])
        self.assertEqual(response_2.context["ad"].description, form_new_data["description"])
        self.assertEqual(response_2.context["ad"].image_url, form_new_data["image_url"])
        self.assertEqual(response_2.context["ad"].category, form_new_data["category"])
        self.assertEqual(response_2.context["ad"].condition, form_new_data["condition"])

    def test_update_not_owned_ad(self):
        form_data = {
            "title": "Test ad title.",
            "description": "Test ad description",
            "image_url": "https://www.python.org/static/img/python-logo.png",
            "category": "Test ad",
            "condition": "For tests only!"
        }
        Ad.objects.create(user=self.user_2, **form_data)
        form_new_data = {
            "title": "New test ad title.",
            "description": "New test ad description",
            "image_url": "https://www.python.org/static/img/psf-logo.png",
            "category": "New test ad",
            "condition": "New for tests only!",
            "_method": "PUT"
        }
        response_1 = self.client.post(reverse("ads:ad_edit", kwargs={"pk": Ad.objects.last().id}), form_new_data)
        self.assertEqual(response_1.status_code, 403)

        response_2 = self.client.get(reverse("ads:ad_detail", kwargs={"pk": Ad.objects.last().id}))
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(response_2.context["ad"].title, form_data["title"])
        self.assertEqual(response_2.context["ad"].description, form_data["description"])
        self.assertEqual(response_2.context["ad"].image_url, form_data["image_url"])
        self.assertEqual(response_2.context["ad"].category, form_data["category"])
        self.assertEqual(response_2.context["ad"].condition, form_data["condition"])

    def test_can_delete_ad(self):
        form_data = {
            "title": "Test ad title.",
            "description": "Test ad description",
            "image_url": "https://www.python.org/static/img/python-logo.png",
            "category": "Test ad",
            "condition": "For tests only!"
        }
        ad_to_delete = Ad.objects.create(user=self.user_1, **form_data)
        ad_to_delete_id = ad_to_delete.id
        response_1 = self.client.delete(reverse("ads:ad_delete", kwargs={"pk": Ad.objects.last().id}))
        self.assertTrue(response_1.status_code, 200)
        self.assertRedirects(response_1, reverse("ads:ads"))

        response_2 = self.client.get(reverse("ads:ad_detail", kwargs={"pk": ad_to_delete_id}))
        self.assertTrue(response_2.status_code, 404)

    def test_can_delete_not_owned_ad(self):
        form_data = {
            "title": "Test ad title.",
            "description": "Test ad description",
            "image_url": "https://www.python.org/static/img/python-logo.png",
            "category": "Test ad",
            "condition": "For tests only!"
        }
        ad_to_delete = Ad.objects.create(user=self.user_1, **form_data)
        ad_to_delete_id = ad_to_delete.id
        response_1 = self.client.delete(reverse("ads:ad_delete", kwargs={"pk": Ad.objects.last().id}))
        self.assertTrue(response_1.status_code, 403)

        response_2 = self.client.get(reverse("ads:ad_detail", kwargs={"pk": ad_to_delete_id}))
        self.assertTrue(response_2.status_code, 200)

    def test_can_delete_unknown_ad(self):
        form_data = {
            "title": "Test ad title.",
            "description": "Test ad description",
            "image_url": "https://www.python.org/static/img/python-logo.png",
            "category": "Test ad",
            "condition": "For tests only!"
        }
        Ad.objects.create(user=self.user_2, **form_data)
        response_1 = self.client.delete(reverse("ads:ad_delete", kwargs={"pk": Ad.objects.last().id + 1}))
        self.assertTrue(response_1.status_code, 404)


class TestExchangeProposal(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(username="test_user_1", password="test_user_password")
        self.user_2 = User.objects.create_user(username="test_user_2", password="test_user_password")
        self.client.force_login(self.user_1)
