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
    path('api/shops-by-category-and-city/', api_views.get_shop_by_category_and_city, name='shops-by-category-and-city'),
    path('api/shops-by-city/', api_views.get_shop_by_city, name='shops-by-city'),
    path('shop-by-category/<int:cat>/', views.shop_by_cat, name='shop-by-cat'),
    path('api/search-shop/<str:query>/',api_views.search_for_shop, name='search'),
    path('create-buy-in/<str:slot_id>',views.create_buy_in_booking, name='buy-in'),
    path('create-pickup-in/<str:slot_id>',views.create_pick_up_booking, name='pick-up'),
    path('api/pickup-notification/', api_views.create_notification, name= 'pick-up-notification'),
    path('api/get-shop-details/<str:gst_id>/', api_views.get_shop_details, name='get-shop-details'),
    path('api/change-shop-start-time/<str:gst_id>/', api_views.change_shop_start_time, name= 'change-shop-start-time'),
    path('api/change-shop-stop-time/<str:gst_id>/', api_views.change_shop_stop_time, name= 'change-shop-stop-time'),
    path('api/add-break-day/<str:gst_id>/', api_views.add_day_break, name= 'add-daybreak'),
    path('is-next-day-off/<str:gst_id>/', api_views.is_next_day_off, name='is-next-day-off')
]