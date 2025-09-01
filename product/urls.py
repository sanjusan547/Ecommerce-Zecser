from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ProductView,CategoryView,VariantView

router=DefaultRouter()
router.register('categories',CategoryView)
router.register('productvariant',VariantView)
router.register('product',ProductView)

urlpatterns = [
   path('',include(router.urls))
]
