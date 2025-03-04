from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


swagger_view = SpectacularSwaggerView.as_view(url_name='schema')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('cart.urls')),
    path('api/', include('products.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'login/',
        TemplateView.as_view(template_name='login.html'),
        name='login'
    ),
    path(
        '',
        TemplateView.as_view(template_name='index.html'),
        name='index'
    ),
    path(
        'api/docs/',
        TemplateView.as_view(template_name='docs.html'),
        name='api-docs'
    ),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', swagger_view, name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
        )
