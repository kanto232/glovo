from rest_framework import serializers
from .models import (UserProfile, Category, SubCategory, Store, Contact, Address, StoreMenu,
                     Product, Order, Courier, Review)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "first_name", "last_name"]


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_image']



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'contact_name', 'contact_number']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'address_name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_image', 'product_description', 'price',
                  'quantity']

class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory_image', 'subcategory_name']

class StoreListSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    good_review = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()
    class Meta:
        model = Store
        fields = ['id', 'store_image', 'store_name', 'average_rating', 'good_review', 'count_people']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_good_review(self, obj):
        return obj.get_good_review()

    def get_count_people(self, obj):
        return obj.get_count_people()


class CategoryDetailSerializer(serializers.ModelSerializer):
    subcategory_category = SubCategoryListSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'subcategory_category']



class SubCategoryDetailSerializer(serializers.ModelSerializer):
    store_subcategory = StoreListSerializer(many=True, read_only=True)
    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory_image', 'subcategory_name', 'store_subcategory']



class StoreMenuListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreMenu
        fields = ['id', 'menu_name']


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderListSerializer(serializers.ModelSerializer):
    products = ProductSerializer()
    class Meta:
        model = Order
        fields = ['id', 'products', 'status']

class OrderDetailSerializer(serializers.ModelSerializer):
    products = ProductSerializer()
    courier = UserProfileSimpleSerializer()
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%S")

    class Meta:
        model = Order
        fields = ['id', 'products', 'status', 'delivery_address', 'courier', 'created_at']



class CourierListSerializer(serializers.ModelSerializer):
    current_orders = OrderListSerializer()
    class Meta:
        model = Courier
        fields = ['id', 'current_orders', 'courier_status']


class StoreMenuDetailSerializer(serializers.ModelSerializer):
    store_product = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = StoreMenu
        fields = ['id', 'menu_name', 'store_product']


class ReviewCreateEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    client = UserProfileSimpleSerializer()
    created_date = serializers.DateTimeField(format="%d-%m-%Y %H:%S")
    class Meta:
        model = Review
        fields = ['id', 'client', 'rating', 'text', 'created_date']

class StoreDetailSerializer(serializers.ModelSerializer):
    store_menu = StoreMenuDetailSerializer(many=True, read_only=True)
    store_contact = ContactSerializer(many=True, read_only=True)
    store_address = AddressSerializer(many=True, read_only=True)
    good_review = serializers.SerializerMethodField()
    owner = UserProfileSimpleSerializer()
    review_store = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Store
        fields = ['id', 'store_image', 'store_name', 'store_menu', 'store_contact', 'store_address',
                  'description', 'owner', 'created_date', 'good_review', 'review_store']

    def get_good_review(self, obj):
        return obj.get_good_review()