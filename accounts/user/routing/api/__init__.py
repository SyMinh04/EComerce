from django.urls import include, path


urlpatterns = [
    path('space/account/', include('accounts.user.routing.api.space_urls')),
]
