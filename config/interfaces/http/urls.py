from django.contrib import admin
from django.urls import path

from config.interfaces.http import views

urlpatterns = [
    path("", views.dashboard, name="overview"),
    path("module-1/", views.placeholder, {"key": "module-1"}, name="module-1"),
    path("module-2/", views.placeholder, {"key": "module-2"}, name="module-2"),
    path("module-4/", views.placeholder, {"key": "module-4"}, name="module-4"),
    path("sources/", views.placeholder, {"key": "sources"}, name="sources"),
    path("import/", views.placeholder, {"key": "import"}, name="import"),
    path("reports/", views.placeholder, {"key": "reports"}, name="reports"),
    path("admin/", admin.site.urls),
]
