from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from rest_framework import generics
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny,IsAuthenticated
from allauth.socialaccount.models import SocialToken , SocialAccount
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product, Category
from .serializer import ProductSerializer, CategorySerializer , UserSerializer
from .services import recommend_products_service, import_data_service
from django.contrib.auth.models import User
# User 
User = get_user_model()

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class UserDashboardView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        #prepare user data
        user_data = {
            'id': user.id,
            'username': user.username,
            'is_staff': user.is_staff,
            'is_active': user.is_active
        }

        return Response(user_data)

@login_required
def google_login_callback(request):
    user = request.user
    social_accounts = SocialAccount.objects.filter(user = user)
    print('Social Account for user:',social_accounts)
    social_account = social_accounts.first()
    if not social_account:
        print('No social account for user: ',user)
        return redirect('http://localhost:5173/login/callback/?error=NoSocialAccount')
    token = SocialToken.objects.filter(account = social_account,account__providers = 'google').first()
    if token : 
        print(f'Google token found : {token.token}')
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return redirect(f'http://localhost:5173/login/callback/?access_token={access_token}')
    else : 
        print('No Google Token found for user : ',user)
        return redirect(f'http://localhost:5173/login/callback/?error=NoGoogleToken')
@csrf_exempt
def validate_google_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            google_access_token = data.get('access_token')
            print(google_access_token)
            if not google_access_token :
                return JsonResponse({'detail':'Access Token is missing'},status=400)
            return JsonResponse({'valid': True})
        except json.JSONDecodeError :
            return JsonResponse({'detail':'invalid Json'},status=400)
    return JsonResponse({'detail':'Method not Allowed'},status=405)

# ----------------  THOSE VIEWS ARE PUBLIC  ---------------- 
# get recommend products
@api_view(['POST'])
@permission_classes([AllowAny])
def recommend_products(request):
    search_words = request.data.get('query', '')
    if not search_words:
        return Response({"error": "Query parameter is missing"}, status=400)
    recommended_products = recommend_products_service(search_words)
    return Response({"recommended_products": recommended_products})

#get categories 
@api_view(['GET'])
@permission_classes([AllowAny])
def getCategories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories,many=True) # to pass the absolute path
    return Response(serializer.data)
# get all products
@api_view(['GET'])
@permission_classes([AllowAny])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products,many=True)
    return Response(serializer.data)

#get products by category
@api_view(['GET'])
@permission_classes([AllowAny])
def getProductsByCategory(request , category_name):
    id_category =Category.objects.filter(name=category_name)[0]
    products = Product.objects.filter(category=id_category)
    serializer = ProductSerializer(products,many=True)
    return Response(serializer.data)

#get product by id
@api_view(['GET'])
@permission_classes([AllowAny])
def get_product_detail(request ,product_id):
    product = Product.objects.filter(id=product_id)
    serializer = ProductSerializer(product,many=True)
    return Response(serializer.data)
# get most popular products
@api_view(['GET'])
@permission_classes([AllowAny])
def get_most_popular_products(request):
    top_rated_products = Product.objects.order_by('-rating')[:8]
    # Serialize and return the products
    serializer = ProductSerializer(top_rated_products, many=True)
    return Response(serializer.data)
def import_data(request):
    import_data_service()