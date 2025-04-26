from django.test import TestCase
from django.contrib.auth.models import User
from ads.forms import NewAdForm, NewExchangeProposalForm
from ads.models import Ad, ExchangeProposal
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

    def test_create_view_can_create_with_correct_form_with_image_url(self):
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

    def test_create_view_can_create_with_correct_form_without_image_url(self):
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

    def test_create_view_cant_create_with_correct_form_without_login(self):
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

    def test_create_view_cant_create_with_invalid_form_without_title(self):
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

    def test_create_view_cant_create_with_invalid_form_without_description(self):
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

    def test_create_view_cant_create_with_invalid_form_without_category(self):
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

    def test_create_view_cant_create_with_invalid_form_without_condition(self):
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

    def test_list_view_can_get_empty_ads_list(self):
        response = self.client.get(reverse("ads:ads"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["ads"]), 0)

    def test_list_view_can_get_many_ads_list(self):
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

    def test_detail_view_can_get_ad(self):
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

    def test_detail_view_can_get_non_existent_ad(self):
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

    def test_edit_view_can_edit_ad_with_correct_form(self):
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

    def test_edit_view_cant_edit_not_owned_ad(self):
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

    def test_delete_view_can_delete_ad(self):
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

    def test_delete_view_cant_delete_not_owned_ad(self):
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

    def test_delete_view_cant_delete_non_existent_ad(self):
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

    def generate_ad_form(self, index):
        return {i_key: i_value.format(index) for i_key, i_value in self.ad_template_form_data.items()}

    def setUp(self):
        self.ad_template_form_data = {
            "title": "Ad {}",
            "description": "Test ad {} description",
            "category": "Test ad {}",
            "condition": "{} For tests only!"
        }
        self.user_1 = User.objects.create_user(username="test_user_1", password="test_user_password")
        self.user_2 = User.objects.create_user(username="test_user_2", password="test_user_password")
        self.user_3 = User.objects.create_user(username="test_user_3", password="test_user_password")
        self.ad_1 = Ad.objects.create(user=self.user_1, **self.generate_ad_form(1))
        self.ad_2 = Ad.objects.create(user=self.user_2, **self.generate_ad_form(2))
        self.ad_3 = Ad.objects.create(user=self.user_3, **self.generate_ad_form(3))
        self.client.force_login(self.user_1)

    def test_valid_form_with_comment(self):
        exchange_form_data = {
            "ad_sender": self.ad_1.id,
            "ad_receiver": self.ad_2.id,
            "comment": "Test comment"
        }
        form = NewExchangeProposalForm(data=exchange_form_data)
        self.assertTrue(form.is_valid())

    def test_valid_form_without_ad_sender(self):
        exchange_form_data = {
            "ad_sender": "",
            "ad_receiver": self.ad_2.id,
            "comment": "Test comment"
        }
        form = NewExchangeProposalForm(data=exchange_form_data)
        self.assertTrue(form.has_error("ad_sender"))
        self.assertFalse(form.is_valid())

    def test_valid_form_with_invalid_ad_sender(self):
        exchange_form_data = {
            "ad_sender": "Text is not id",
            "ad_receiver": self.ad_2.id,
            "comment": "Test comment"
        }
        form = NewExchangeProposalForm(data=exchange_form_data)
        self.assertTrue(form.has_error("ad_sender"))
        self.assertFalse(form.is_valid())

    def test_valid_form_without_ad_receiver(self):
        exchange_form_data = {
            "ad_sender": self.ad_1.id,
            "ad_receiver": "",
            "comment": "Test comment"
        }
        form = NewExchangeProposalForm(data=exchange_form_data)
        self.assertTrue(form.has_error("ad_receiver"))
        self.assertFalse(form.is_valid())

    def test_valid_form_with_invalid_ad_receiver(self):
        exchange_form_data = {
            "ad_sender": self.ad_1.id,
            "ad_receiver": "Text is not id",
            "comment": "Test comment"
        }
        form = NewExchangeProposalForm(data=exchange_form_data)
        self.assertTrue(form.has_error("ad_receiver"))
        self.assertFalse(form.is_valid())

    def test_valid_form_without_comment(self):
        exchange_form_data = {
            "ad_sender": self.ad_1.id,
            "ad_receiver": self.ad_2.id,
            "comment": ""
        }
        form = NewExchangeProposalForm(data=exchange_form_data)
        self.assertTrue(form.has_error("comment"))
        self.assertFalse(form.is_valid())

    def test_create_view_can_create_with_correct_form(self):
        exchange_form_data = {
            "ad_sender": self.ad_1.id,
            "ad_receiver": self.ad_2.id,
            "comment": "Test comment"
        }
        response_1 = self.client.post(reverse("ads:new_exchange"), data=exchange_form_data)
        self.assertEqual(response_1.status_code, 302)
        self.assertRedirects(response_1, reverse("ads:exchange_confirmation"))

        response_2 = self.client.post(reverse("ads:exchange_confirmation"))
        self.assertEqual(response_2.status_code, 302)
        self.assertEqual(ExchangeProposal.objects.last().ad_sender, self.ad_1)
        self.assertEqual(ExchangeProposal.objects.last().ad_receiver, self.ad_2)
        self.assertRedirects(response_2, reverse("ads:exchange_detail", kwargs={"pk": ExchangeProposal.objects.last().id}))

    def test_create_view_cant_create_with_correct_form_without_login(self):
        self.client.logout()
        exchange_form_data = {
            "ad_sender": self.ad_1.id,
            "ad_receiver": self.ad_2.id,
            "comment": "Test comment"
        }
        response_1 = self.client.post(reverse("ads:new_exchange"), data=exchange_form_data)
        self.assertEqual(response_1.status_code, 302)
        self.assertRedirects(response_1, reverse("users:login"))

    def test_create_view_cant_create_with_invalid_form_without_ad_sender(self):
        exchange_form_data = {
            "ad_sender": "",
            "ad_receiver": self.ad_2.id,
            "comment": "Test comment"
        }
        response = self.client.post(reverse("ads:new_exchange"), data=exchange_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["form"].errors), 1)
        self.assertEqual(response.context["form"].errors["ad_sender"][0], "Обязательное поле.")

    def test_create_view_cant_create_with_invalid_form_without_ad_receiver(self):
        exchange_form_data = {
            "ad_sender": self.ad_1.id,
            "ad_receiver": "",
            "comment": "Test comment"
        }
        response = self.client.post(reverse("ads:new_exchange"), data=exchange_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["form"].errors), 1)
        self.assertEqual(response.context["form"].errors["ad_receiver"][0], "Обязательное поле.")

    def test_create_view_cant_create_with_invalid_form_without_comment(self):
        exchange_form_data = {
            "ad_sender": self.ad_1.id,
            "ad_receiver": self.ad_2.id,
            "comment": ""
        }
        response = self.client.post(reverse("ads:new_exchange"), data=exchange_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["form"].errors), 1)
        self.assertEqual(response.context["form"].errors["comment"][0], "Обязательное поле.")

    def test_create_view_cant_create_duplicate_with_correct_forms(self):
        exchange_form_data = {
            "ad_sender": self.ad_1.id,
            "ad_receiver": self.ad_2.id,
            "comment": "Test comment"
        }
        response_1 = self.client.post(reverse("ads:new_exchange"), data=exchange_form_data)
        self.assertEqual(response_1.status_code, 302)
        self.assertRedirects(response_1, reverse("ads:exchange_confirmation"))

        response_2 = self.client.post(reverse("ads:exchange_confirmation"))
        self.assertEqual(response_2.status_code, 302)
        self.assertEqual(ExchangeProposal.objects.last().ad_sender, self.ad_1)
        self.assertEqual(ExchangeProposal.objects.last().ad_receiver, self.ad_2)
        self.assertRedirects(response_2, reverse("ads:exchange_detail", kwargs={"pk": ExchangeProposal.objects.last().id}))

        response_3 = self.client.post(reverse("ads:new_exchange"), data=exchange_form_data)
        self.assertEqual(response_3.status_code, 200)
        self.assertEqual(response_3.context["form"].errors["ad_sender"][0], f"Предложение обмена {self.ad_1.id} на {self.ad_2.id} уже существует")
        self.assertIn("Предложение обмена 1", response_3.context["form"].errors["ad_sender"][1])
        self.assertIn(reverse("ads:exchange_detail", kwargs={"pk": 1}), response_3.context["form"].errors["ad_sender"][1])

        self.client.force_login(self.user_2)
        counter_exchange_form_data = {
            "ad_sender": self.ad_2.id,
            "ad_receiver": self.ad_1.id,
            "comment": "Test comment"
        }
        response_4 = self.client.post(reverse("ads:new_exchange"), data=counter_exchange_form_data)
        self.assertEqual(response_4.status_code, 200)
        self.assertEqual(response_4.context["form"].errors["ad_sender"][0], f"Предложение обмена {self.ad_2.id} на {self.ad_1.id} уже существует")
        self.assertIn("Предложение обмена 1", response_3.context["form"].errors["ad_sender"][1])
        self.assertIn(reverse("ads:exchange_detail", kwargs={"pk": 1}), response_3.context["form"].errors["ad_sender"][1])

    def test_create_view_cant_propose_not_owned_ad(self):
        exchange_form_data = {
            "ad_sender": self.ad_2.id,
            "ad_receiver": self.ad_1.id,
            "comment": "Test comment"
        }
        response = self.client.post(reverse("ads:new_exchange"), data=exchange_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["form"].errors["ad_sender"][0], f"Этот товар вам не принадлежит. Список доступных товаров: 1")

    def test_create_view_cant_propose_to_owned_ad(self):
        new_ad = Ad.objects.create(user=self.user_1, **self.generate_ad_form(4))
        exchange_form_data = {
            "ad_sender": self.ad_1.id,
            "ad_receiver": new_ad.id,
            "comment": "Test comment"
        }
        response = self.client.post(reverse("ads:new_exchange"), data=exchange_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["form"].errors["ad_receiver"][0], f"Нельзя обмениваться на свои товары.")

    def test_create_view_cant_propose_non_existent_ad(self):
        exchange_form_data = {
            "ad_sender": Ad.objects.last().id + 1,
            "ad_receiver": self.ad_2.id,
            "comment": "Test comment"
        }
        response = self.client.post(reverse("ads:new_exchange"), data=exchange_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["form"].errors["ad_sender"][0], f"Товара не существует.")

    def test_create_view_cant_propose_to_non_existent_ad(self):
        exchange_form_data = {
            "ad_sender": self.ad_1.id,
            "ad_receiver": Ad.objects.last().id + 1,
            "comment": "Test comment"
        }
        response = self.client.post(reverse("ads:new_exchange"), data=exchange_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["form"].errors["ad_receiver"][0], f"Товара не существует.")

    def test_list_view_can_get_empty_exchanges_list(self):
        response = self.client.get(reverse("ads:exchanges"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["exchanges_list"]), 0)

    def test_list_view_can_get_many_exchanges_list(self):
        exchange_form_data = {
            "ad_receiver": self.ad_2,
            "comment": "Test comment"
        }
        for i_index in range(20):
            exchange_form_data["ad_sender"] = Ad.objects.create(user=self.user_1, **self.generate_ad_form(i_index))
            ExchangeProposal.objects.create(**exchange_form_data)

        response_1 = self.client.get(reverse("ads:exchanges"))
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(len(response_1.context["exchanges_list"]), 15)

        response_2 = self.client.get(f"{reverse("ads:exchanges")}?page=2")
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(len(response_2.context["exchanges_list"]), 5)

    def test_detail_view_can_get_not_owned_exchange(self):
        exchange_form_data = {
            "ad_sender": self.ad_2,
            "ad_receiver": self.ad_3,
            "comment": "Test comment"
        }
        ExchangeProposal.objects.create(**exchange_form_data)

        response_1 = self.client.get(reverse("ads:exchanges"))
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(len(response_1.context["exchanges_list"]), 0)

        self.client.force_login(self.user_2)
        response_2 = self.client.get(reverse("ads:exchanges"))
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(len(response_2.context["exchanges_list"]), 1)

        self.client.force_login(self.user_3)
        response_3 = self.client.get(reverse("ads:exchanges"))
        self.assertEqual(response_3.status_code, 200)
        self.assertEqual(len(response_3.context["exchanges_list"]), 1)

    def test_detail_view_can_get_exchange(self):
        exchange_form_data = {
            "ad_sender": self.ad_1,
            "ad_receiver": self.ad_2,
            "comment": "Test comment"
        }
        ExchangeProposal.objects.create(**exchange_form_data)

        response = self.client.get(reverse("ads:exchange_detail", kwargs={"pk": ExchangeProposal.objects.last().id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["exchange_proposal"], ExchangeProposal.objects.last())
        self.assertEqual(response.context["exchange_proposal"].ad_sender, self.ad_1)
        self.assertEqual(response.context["exchange_proposal"].ad_receiver, self.ad_2)
        self.assertEqual(response.context["exchange_proposal"].comment, "Test comment")

    def test_detail_view_cant_get_not_owned_exchange(self):
        exchange_form_data = {
            "ad_sender": self.ad_2,
            "ad_receiver": self.ad_3,
            "comment": "Test comment"
        }
        ExchangeProposal.objects.create(**exchange_form_data)

        response = self.client.get(reverse("ads:exchange_detail", kwargs={"pk": ExchangeProposal.objects.last().id}))
        self.assertEqual(response.status_code, 403)

    def test_edit_view_can_edit_with_correct_form(self):
        exchange_form_data = {
            "ad_sender": self.ad_1,
            "ad_receiver": self.ad_2,
            "comment": "Test comment"
        }
        ExchangeProposal.objects.create(**exchange_form_data)

        ad_4 = Ad.objects.create(user=self.user_1, **self.generate_ad_form(4))
        ad_5 = Ad.objects.create(user=self.user_2, **self.generate_ad_form(5))
        new_exchange_form_data = {
            "ad_sender": ad_4.id,
            "ad_receiver": ad_5.id,
            "comment": "New test comment"
        }
        response_1 = self.client.post(reverse("ads:exchange_edit", kwargs={"pk": ExchangeProposal.objects.last().id}), new_exchange_form_data)
        self.assertEqual(response_1.status_code, 302)
        self.assertRedirects(response_1, reverse("ads:exchange_detail", kwargs={"pk": ExchangeProposal.objects.last().id}))

        response_2 = self.client.get(reverse("ads:exchange_detail", kwargs={"pk": ExchangeProposal.objects.last().id}))
        self.assertEqual(response_2.context["exchange_proposal"].ad_sender.id, new_exchange_form_data["ad_sender"])
        self.assertEqual(response_2.context["exchange_proposal"].ad_receiver.id, new_exchange_form_data["ad_receiver"])
        self.assertEqual(response_2.context["exchange_proposal"].comment, new_exchange_form_data["comment"])

    def test_edit_view_cant_edit_not_owned_ad(self):
        exchange_form_data = {
            "ad_sender": self.ad_2,
            "ad_receiver": self.ad_3,
            "comment": "Test comment"
        }
        ExchangeProposal.objects.create(**exchange_form_data)
        ad_4 = Ad.objects.create(user=self.user_1, **self.generate_ad_form(4))
        ad_5 = Ad.objects.create(user=self.user_2, **self.generate_ad_form(5))
        ad_6 = Ad.objects.create(user=self.user_3, **self.generate_ad_form(5))
        new_exchange_form_data_1 = {
            "ad_sender": ad_4.id,
            "ad_receiver": ad_5.id,
            "comment": "New test comment"
        }
        response_1 = self.client.post(reverse("ads:exchange_edit", kwargs={"pk": ExchangeProposal.objects.last().id}), new_exchange_form_data_1)
        self.assertEqual(response_1.status_code, 403)
        self.client.force_login(self.user_3)

        new_exchange_form_data_2 = {
            "ad_sender": ad_6.id,
            "ad_receiver": ad_5.id,
            "comment": "New test comment"
        }
        response_2 = self.client.post(reverse("ads:exchange_edit", kwargs={"pk": ExchangeProposal.objects.last().id}), new_exchange_form_data_2)
        self.assertEqual(response_2.status_code, 403)

        self.client.force_login(self.user_2)
        response_3 = self.client.get(reverse("ads:exchange_edit", kwargs={"pk": ExchangeProposal.objects.last().id}))
        self.assertEqual(response_3.status_code, 200)
        self.assertEqual(response_3.context["exchange_proposal"].ad_sender, exchange_form_data["ad_sender"])
        self.assertEqual(response_3.context["exchange_proposal"].ad_receiver, exchange_form_data["ad_receiver"])
        self.assertEqual(response_3.context["exchange_proposal"].comment, exchange_form_data["comment"])

    def test_edit_view_cant_edit_non_existence_exchange(self):
        exchange_form_data = {
            "ad_sender": self.ad_2,
            "ad_receiver": self.ad_3,
            "comment": "Test comment"
        }
        ExchangeProposal.objects.create(**exchange_form_data)
        ad_4 = Ad.objects.create(user=self.user_1, **self.generate_ad_form(4))
        ad_5 = Ad.objects.create(user=self.user_2, **self.generate_ad_form(5))
        new_exchange_form_data = {
            "ad_sender": ad_4.id,
            "ad_receiver": ad_5.id,
            "comment": "New test comment"
        }
        response = self.client.post(reverse("ads:exchange_edit", kwargs={"pk": ExchangeProposal.objects.last().id}), new_exchange_form_data)
        self.assertEqual(response.status_code, 403)

    def test_delete_view_can_delete_exchange(self):
        exchange_form_data = {
            "ad_sender": self.ad_1,
            "ad_receiver": self.ad_2,
            "comment": "Test comment"
        }
        exchange_to_delete = ExchangeProposal.objects.create(**exchange_form_data)
        exchange_to_delete_id = exchange_to_delete.id
        response_1 = self.client.delete(reverse("ads:exchange_delete", kwargs={"pk": exchange_to_delete_id}))
        self.assertTrue(response_1.status_code, 200)
        self.assertRedirects(response_1, reverse("ads:exchanges"))

        response_2 = self.client.get(reverse("ads:exchange_delete", kwargs={"pk": exchange_to_delete_id}))
        self.assertTrue(response_2.status_code, 403)

        response_3 = self.client.get(reverse("ads:exchanges"))
        self.assertEqual(response_3.status_code, 200)
        self.assertEqual(len(response_3.context["exchanges_list"]), 0)

    def test_delete_view_cant_delete_not_owned_exchange(self):
        exchange_form_data = {
            "ad_sender": self.ad_2,
            "ad_receiver": self.ad_3,
            "comment": "Test comment"
        }
        exchange_to_delete = ExchangeProposal.objects.create(**exchange_form_data)
        exchange_to_delete_id = exchange_to_delete.id

        response_1 = self.client.delete(reverse("ads:exchange_delete", kwargs={"pk": exchange_to_delete_id}))
        self.assertTrue(response_1.status_code, 403)

        self.client.force_login(self.user_3)
        response_2 = self.client.delete(reverse("ads:exchange_delete", kwargs={"pk": exchange_to_delete_id}))
        self.assertTrue(response_2.status_code, 403)

        response_3 = self.client.get(reverse("ads:exchanges"))
        self.assertEqual(response_3.status_code, 200)
        self.assertEqual(response_3.context["exchanges_list"][0], exchange_to_delete)

    def test_delete_view_cant_delete_non_existent_exchange(self):
        exchange_form_data = {
            "ad_sender": self.ad_1,
            "ad_receiver": self.ad_2,
            "comment": "Test comment"
        }
        ExchangeProposal.objects.create(**exchange_form_data)
        response_1 = self.client.delete(reverse("ads:ad_delete", kwargs={"pk": ExchangeProposal.objects.last().id + 1}))
        self.assertTrue(response_1.status_code, 403)
