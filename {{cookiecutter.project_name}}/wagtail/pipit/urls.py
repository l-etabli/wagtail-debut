{% if cookiecutter.use_grapple == "yes" %}from django.apps import apps{% endif %}
from django.contrib import admin
from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.views import defaults as default_views
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls
from wagtail.contrib.sitemaps.views import sitemap

{% if cookiecutter.use_grapple == "yes" %}from grapple import urls as grapple_urls{% endif %}

from main.views.page_not_found import PageNotFoundView
from main.views.error_500 import error_500_view
{% if cookiecutter.use_decoupled_frontend == "yes" %}from nextjs.api import api_router{% endif %}


handler404 = PageNotFoundView.as_view()
handler500 = error_500_view

urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        path(
            "wt/400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),  # NOQA
        path(
            "wt/403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),  # NOQA
        path(
            "wt/404/", handler404, kwargs={"exception": Exception("Page not Found")}
        ),  # NOQA
        path(
            "wt/500/", handler500, kwargs={"exception": Exception("Internal error")}
        ),  # NOQA
    ]

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [path("wt/__debug__/", include(debug_toolbar.urls))]  # type: ignore


{% if cookiecutter.use_django_pattern_library == "yes" %}if apps.is_installed("pattern_library"):
    urlpatterns += [
        path("pattern-library/", include("pattern_library.urls")),
    ]{% endif %}

{% if cookiecutter.use_grapple == "yes" %}urlpatterns += [
    path("", include(grapple_urls)),
]{% endif %}


urlpatterns += [
    path(settings.ADMIN_URL, admin.site.urls),
    {% if cookiecutter.use_decoupled_frontend == "yes" %}path("wt/api/nextjs/v1/", api_router.urls),{% endif %}
    path("wt/cms/", include(wagtailadmin_urls)),  # type: ignore
    path("wt/documents/", include(wagtaildocs_urls)),  # type: ignore
    path("wt/sitemap.xml", sitemap, name="sitemap"),
]

urlpatterns += [re_path(r"", include(wagtail_urls))]  # type: ignore

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
