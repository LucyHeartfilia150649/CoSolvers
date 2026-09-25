from django.test import TestCase
from django.test import override_settings
from unittest.mock import Mock, patch

from django.contrib.auth.models import User


@override_settings(
	RECAPTCHA_SITE_KEY="test-site-key",
	RECAPTCHA_SECRET_KEY="test-secret-key",
)
class SignUpEmailDomainTests(TestCase):

	def setUp(self):
		self.recaptcha_response = Mock(ok=True)
		self.recaptcha_response.json.return_value = {"success": True}

	def signup(self, email):
		return self.client.post(
			"/sign_up/",
			{
				"student_id": "user123",
				"email": email,
				"password": "StrongPass1!",
				"faculty": "Engineering",
				"g-recaptcha-response": "test-token",
			},
		)

	@patch("COSOLVERS_app.views.requests.post")
	def test_allows_student_and_staff_chula_email_domains(self, post):
		post.return_value = self.recaptcha_response

		for index, email in enumerate(
			["student@student.chula.ac.th", "staff@chula.ac.th"]
		):
			response = self.signup(email)

			self.assertRedirects(response, "/profile/")
			self.assertTrue(User.objects.filter(email=email).exists())
			if index == 0:
				self.client.get("/logout/")

	@patch("COSOLVERS_app.views.requests.post")
	def test_rejects_personal_email_with_red_error_message(self, post):
		post.return_value = self.recaptcha_response

		response = self.signup("user@gmail.com")

		self.assertEqual(response.status_code, 200)
		self.assertContains(
			response,
			"กรุณาใช้อีเมลของจุฬาลงกรณ์มหาวิทยาลัยเท่านั้น",
		)
		self.assertContains(response, 'class="message error"')
		self.assertFalse(User.objects.filter(email="user@gmail.com").exists())

# Create your tests here.
