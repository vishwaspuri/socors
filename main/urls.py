from django.urls import path
from main.api import api_views
from main import views

urlpatterns = [
    path('',views.BaseView.as_view(),name='home' ),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('mytimeslots/', views.MytimeslotsView.as_view(), name='mytimeslots'),
    path('notifications/', views.NotificationView.as_view(), name='notifications'),
    path('shops-near-me/', views.shop_near_me, name='explore'),
    path('shops-slots/<str:gst_id>/', views.shop_slots, name='shop-slots'),
    path('api/shop-list/<int:pin>/', api_views.ShopView.as_view(), name='shops'),
    path('api/shop-slots/<str:gst_id>/', api_views.list_slots_for_shop, name='slots'),
    path('api/book-slot/', api_views.book_slot, name='shops'),
    path('api/user-bookings/', api_views.user_booked_slots, name='user-slots'),
    path('api/shops-by-category-and-city/', api_views.get_shop_by_category_and_city, name='shops-by-category-and-city'),
    path('api/shops-by-city/', api_views.get_shop_by_city, name='shops-by-city'),
    path('shop-by-category/<int:cat>/', views.shop_by_cat, name='shop-by-cat'),
    path('api/search-shop/<str:query>/',api_views.search_for_shop, name='search')
]