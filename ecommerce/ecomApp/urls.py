from django.urls import path ,include
from ecomApp import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


urlpatterns = [
    path('products',views.getProducts,name='getProducts'),
    path('categories',views.getCategories,name='getCategories'),
    path('categories/<str:category_name>/products/',views.getProductsByCategory, name='getProductsByCategory'),
    path('product/<int:product_id>/', views.get_product_detail, name='get_product_detail'),
    path('highest-rated-products/', views.get_most_popular_products, name='get_most_popular_products'),
    path('recommend-products/', views.recommend_products, name='recommend-products'),
    path('import-data/', views.import_data, name='import_data'),
    path('accounts/',include('allauth.urls')),
    path('api-auth/',include('rest_framework.urls')),
    path('auth/user/register/', views.UserCreate.as_view(),name='user_create'),
    path('auth/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('auth/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('callback/', views.google_login_callback,name='callback'),
    path('auth/user/',views.UserDetailView.as_view(),name='user-detail'),
    path('auth/google/validate_token',views.validate_google_token,name='validate-token'),
    path('dashboard/', views.UserDashboardView.as_view(), name='dashboard'),
    # path('cart/', CartView.as_view(), name='cart'),
]