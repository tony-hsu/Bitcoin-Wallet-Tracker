import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "bitcoin_wallet_tracker.users"
    verbose_name = _("Users")

    def ready(self):
        with contextlib.suppress(ImportError):
            import bitcoin_wallet_tracker.users.signals  # noqa: F401
