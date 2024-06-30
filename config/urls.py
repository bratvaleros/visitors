from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
                  path(settings.ADMIN_URL, admin.site.urls),
                  # Your stuff: custom urls includes go here
                  path('api/v1/', include('visit_control.api_v1.urls', namespace='api_v1')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "403_csrf/",
            TemplateView.as_view(template_name="403_csrf.html"),
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        urlpatterns = [path("__debug__/", include("debug_toolbar.urls"))] + urlpatterns

admin.site.site_header = 'Панель управления Visit Control'  # default: "Django Administration"
admin.site.index_title = 'Панель управления'  # default: "Site administration"
admin.site.site_title = 'Панель управления Visit Control'  # default: "Django site admin"
