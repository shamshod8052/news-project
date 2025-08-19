from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class OnlyLoggedSuperUser(UserPassesTestMixin, LoginRequiredMixin):
    def test_func(self):
        return self.request.user.is_superuser
