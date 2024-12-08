from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MarketplacePy.accounts'

    def ready(self):
        import MarketplacePy.accounts.signals
