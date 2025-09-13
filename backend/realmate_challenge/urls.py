from django.urls import path, include

urlpatterns = [
    path("", include("apps.conversation.urls")),
    path("auth/", include("apps.authenticate.urls")),
]