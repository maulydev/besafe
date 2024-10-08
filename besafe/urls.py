from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers
from health_question.views import QuestionViewSet
from advice.views import AdviceViewSet
from health_profile.views import ProfileViewSet, RegisterViewSet, CustomTokenObtainPairView
from analyzer.views import process_data



router = routers.DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'advices', AdviceViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'auth/register', RegisterViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="BeSafe API",
      default_version='v1',
      description="Digital Wellbeing API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('analyzer/', process_data, name='process-data'),
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
