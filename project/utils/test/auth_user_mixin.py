from django.contrib.auth import get_user_model

User = get_user_model()


class AuthUserTestMixin:
    user = None

    def auth_user(self, user=None):
        user = user or self.user
        if not user:
            self.create_user()
            user = self.user

        self.client.force_login(user)

    def create_user(self):
        self.user = User.objects.create_user(
            username='test_user',
            password='test_passwd',
            email='test@mail.com'
        )
