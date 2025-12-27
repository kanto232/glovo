from rest_framework import routers
from django.urls import path, include
from .views import (
    UserProfileListAPIView, UserProfileDetailAPIView, CategoryListAPIView, CategoryDetailAPIView, SubCategoryListAPIView, SubCategoryDetailAPIView, StoreListAPIView, StoreDetailAPIView,ContactViewSet,
    AddressViewSet, RegisterView, CustomLoginView, LogoutView,StoreMenuListAPIView, StoreMenuDetailAPIView, ProductViewSet, OrderCreateAPIView, OrderListAPIView, OrderDetailAPIView,
    CourierViewSet, ReviewCreateAPIView, ReviewEditAPIView
)

router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)
router.register(r'couriers', CourierViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserProfileListAPIView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user-detail'),
    path('category/', CategoryListAPIView.as_view(), name='category-list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('subcategory/', SubCategoryListAPIView.as_view(), name='subcategory-list'),
    path('subcategory/<int:pk>/', SubCategoryDetailAPIView.as_view(), name='subcategory-detail'),
    path('store/', StoreListAPIView.as_view(), name='store-list'),
    path('store/<int:pk>/', StoreDetailAPIView.as_view(), name='store-detail'),
    path('store_menu/', StoreMenuListAPIView.as_view(), name='store_menu-list'),
    path('store_menu/<int:pk>/', StoreMenuDetailAPIView.as_view(), name='store_menu-detail'),
    path('review_create/', ReviewCreateAPIView.as_view(), name='review-create'),
    path('review_create/<int:pk>', ReviewEditAPIView.as_view(), name='review-edit'),
    path('order/', OrderListAPIView.as_view(), name='order-list'),
    path('order/create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('order/<int:pk>', OrderDetailAPIView.as_view(), name='order-detail'),
path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
