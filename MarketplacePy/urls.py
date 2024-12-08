
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('MarketplacePy.accounts.urls')),
    path('', include('MarketplacePy.home.urls')),
    path('items/', include('MarketplacePy.items.urls')),
]
